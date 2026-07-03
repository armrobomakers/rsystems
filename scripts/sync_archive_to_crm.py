from __future__ import annotations

import json
import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4


ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_INDEX = ROOT / "outputs" / "telegram_archive" / "_index.json"
SCHEMA = "workspace_aqgjkvzyjiktitsgg1e0evek1"
CREATED_BY = "Alexandr RYZHKOV"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


CYR_TO_LAT = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "e",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "h",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "sch",
    "ъ": "",
    "ы": "y",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}


@dataclass
class Person:
    id: str
    first_name: str
    last_name: str
    job_title: str


def translit(text: str) -> str:
    out: list[str] = []
    for ch in text:
        out.append(CYR_TO_LAT.get(ch.casefold(), ch))
    return "".join(out)


def clean_name(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "")
    text = text.replace(chr(0xFEFF), "").strip()
    strip_chars = set("[](){}<>\"'")
    strip_chars.update({chr(0x3010), chr(0x3011), chr(0x00AB), chr(0x00BB), chr(0x201C), chr(0x201D)})
    start = 0
    end = len(text)
    while start < end and (text[start].isspace() or text[start] in strip_chars):
        start += 1
    while end > start and (text[end - 1].isspace() or text[end - 1] in strip_chars):
        end -= 1
    text = text[start:end]
    return re.sub(r"\s+", " ", text).strip()


def normalize(text: str) -> str:
    text = clean_name(text)
    text = translit(text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.casefold()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokenize(text: str) -> set[str]:
    return {token for token in normalize(text).split(" ") if token}


def psql(sql: str) -> str:
    result = subprocess.run(
        [
            "docker",
            "exec",
            "-i",
            "-e",
            "PGCLIENTENCODING=UTF8",
            "twenty-db-1",
            "psql",
            "-U",
            "postgres",
            "-d",
            "default",
            "-v",
            "ON_ERROR_STOP=1",
            "-t",
            "-A",
            "-F",
            "\t",
        ],
        input=sql.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = result.stdout.decode("utf-8", errors="replace")
    if result.returncode != 0:
        raise SystemExit(output)
    return output


def fetch_people() -> list[Person]:
    sql = f"""
        SELECT id,
               coalesce("nameFirstName", ''),
               coalesce("nameLastName", ''),
               coalesce("jobTitle", '')
        FROM {SCHEMA}.person
        WHERE "deletedAt" IS NULL
        ORDER BY "createdAt";
    """
    output = psql(sql)
    people: list[Person] = []
    for line in output.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 4:
            continue
        people.append(
            Person(
                id=parts[0],
                first_name=clean_name(parts[1]),
                last_name=clean_name(parts[2]),
                job_title=clean_name(parts[3]),
            )
        )
    return people


def read_index() -> list[dict]:
    if not ARCHIVE_INDEX.exists():
        raise SystemExit(f"Missing archive index: {ARCHIVE_INDEX}")
    return json.loads(ARCHIVE_INDEX.read_text(encoding="utf-8"))


def best_person_match(title: str, people: list[Person]) -> Person | None:
    title = clean_name(title)
    if not title:
        return None

    title_norm = normalize(title)
    title_tokens = tokenize(title)
    if not title_norm or not title_tokens:
        return None

    exact_candidates: list[Person] = []

    for person in people:
        variants = {
            person.first_name,
            person.last_name,
            f"{person.first_name} {person.last_name}".strip(),
        }
        variants = {variant for variant in variants if variant}

        norms = {normalize(variant) for variant in variants if normalize(variant)}
        if title_norm in norms:
            exact_candidates.append(person)

    if exact_candidates:
        exact_candidates.sort(
            key=lambda item: (
                len(normalize(f"{item.first_name} {item.last_name}".strip())),
                1 if item.last_name else 0,
                item.first_name,
                item.last_name,
            )
        )
        return exact_candidates[0]

    if len(title_tokens) == 1:
        token = next(iter(title_tokens))
        direct_matches: list[Person] = []
        for person in people:
            variants = {
                person.first_name,
                person.last_name,
                f"{person.first_name} {person.last_name}".strip(),
            }
            variants = {variant for variant in variants if variant}
            tokens = set().union(*(tokenize(variant) for variant in variants)) if variants else set()
            if token in tokens:
                direct_matches.append(person)

        if len(direct_matches) == 1:
            return direct_matches[0]
        if direct_matches:
            direct_matches.sort(
                key=lambda item: (
                    len(normalize(f"{item.first_name} {item.last_name}".strip())),
                    1 if item.last_name else 0,
                    item.first_name,
                    item.last_name,
                )
            )
            return direct_matches[0]

    return None


def note_exists(archive_id: str) -> bool:
    marker = f"Archive id: {archive_id}"
    marker_sql = marker.replace("'", "''")
    sql = f"""
        SELECT 1
        FROM {SCHEMA}."note"
        WHERE "deletedAt" IS NULL
          AND "bodyV2Markdown" ILIKE '%{marker_sql}%'
        LIMIT 1;
    """
    return bool(psql(sql).strip())


def fetch_recent_lines(folder: Path, limit: int = 8) -> list[str]:
    messages_file = folder / "messages.txt"
    if not messages_file.exists():
        return []
    lines = [line.strip() for line in messages_file.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip()]
    return lines[-limit:]


def insert_note(person_id: str, title: str, body: str) -> None:
    note_id = str(uuid4())
    title_sql = title.replace("'", "''")
    body_sql = body.replace("'", "''")
    sql = f"""
        BEGIN;
        INSERT INTO {SCHEMA}."note" (
          id, title, "bodyV2Markdown",
          "createdBySource", "createdByName", "updatedBySource", "updatedByName"
        ) VALUES (
          '{note_id}', '{title_sql}', '{body_sql}',
          'MANUAL', '{CREATED_BY}', 'MANUAL', '{CREATED_BY}'
        );

        INSERT INTO {SCHEMA}."noteTarget" ("noteId", "targetPersonId")
        VALUES ('{note_id}', '{person_id}');
        COMMIT;
    """
    psql(sql)


def main() -> None:
    people = fetch_people()
    archive = read_index()

    matched = 0
    skipped_existing = 0
    skipped_unmatched = 0

    for item in archive:
        title = clean_name(str(item.get("title", "")))
        archive_id = str(item.get("id", ""))
        folder = ROOT / str(item.get("folder", ""))

        if not title or not archive_id:
            continue

        person = best_person_match(title, people)
        if person is None:
            skipped_unmatched += 1
            continue

        if note_exists(archive_id):
            skipped_existing += 1
            continue

        recent_lines = fetch_recent_lines(folder)
        body_lines = [
            "Telegram archive sync.",
            f"Archive id: {archive_id}",
            f"Dialog: {title}",
            f"Messages in archive: {item.get('messageCount', 0)}",
            f"Matched person: {person.first_name} {person.last_name}".strip(),
            f"Job title: {person.job_title or '-'}",
        ]
        if recent_lines:
            body_lines.append("")
            body_lines.append("Recent messages:")
            body_lines.extend(f"- {line}" for line in recent_lines)

        insert_note(person.id, "Telegram archive sync", "\n".join(body_lines))
        matched += 1
        print(f"+ {title} -> {person.first_name} {person.last_name}".strip())

    print(f"Matched: {matched}")
    print(f"Skipped existing: {skipped_existing}")
    print(f"Skipped unmatched: {skipped_unmatched}")


if __name__ == "__main__":
    main()
