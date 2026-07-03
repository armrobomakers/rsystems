from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4


ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "outputs" / "telegram_users_live.json"
SCHEMA = "workspace_aqgjkvzyjiktitsgg1e0evek1"
CREATED_BY = "Alexandr RYZHKOV"

SKIP_TITLES = {
    "telegram",
    "report impersonation",
    "affy support",
}

SKIP_SUBSTRINGS = {
    "любимая",
    "friends",
}

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


try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


@dataclass
class TelegramUser:
    id: str
    title: str
    first_name: str
    last_name: str
    username: str
    phone: str
    mutual_contact: bool
    contact: bool
    verified: bool
    premium: bool
    status: str
    last_message: str
    last_date: str


def translit(text: str) -> str:
    out: list[str] = []
    for ch in text:
        lower = ch.casefold()
        out.append(CYR_TO_LAT.get(lower, ch))
    return "".join(out)


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "")
    text = translit(text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.casefold()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def clean_name(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "")
    text = text.replace("\ufeff", "").strip()
    text = re.sub(r"^[\s\[\]【】(){}«»\"'“”]+", "", text)
    text = re.sub(r"[\s\[\]【】(){}«»\"'“”]+$", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize(text: str) -> set[str]:
    return {token for token in normalize(text).split(" ") if token}


def load_telegram_users() -> list[TelegramUser]:
    if not JSON_PATH.exists():
        raise SystemExit(f"Missing Telegram dump: {JSON_PATH}")
    raw = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    users: list[TelegramUser] = []
    for row in raw:
        users.append(
            TelegramUser(
                id=str(row.get("id", "")),
                title=clean_name(str(row.get("title", ""))),
                first_name=clean_name(str(row.get("firstName", ""))),
                last_name=clean_name(str(row.get("lastName", ""))),
                username=str(row.get("username", "")).strip().lstrip("@"),
                phone=str(row.get("phone", "")).strip(),
                mutual_contact=bool(row.get("mutualContact", False)),
                contact=bool(row.get("contact", False)),
                verified=bool(row.get("verified", False)),
                premium=bool(row.get("premium", False)),
                status=str(row.get("status", "")).strip(),
                last_message=str(row.get("lastMessage", "")).strip(),
                last_date=str(row.get("lastDate", "")).strip(),
            )
        )
    return users


def fetch_existing_people() -> list[tuple[str, str]]:
    sql = f"""
        SELECT coalesce("nameFirstName", '') AS first_name,
               coalesce("nameLastName", '') AS last_name
        FROM {SCHEMA}.person
        WHERE "deletedAt" IS NULL
        ORDER BY "createdAt";
    """
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

    people: list[tuple[str, str]] = []
    for line in output.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        first = parts[0].strip() if parts else ""
        last = parts[1].strip() if len(parts) > 1 else ""
        people.append((first, last))
    return people


def is_duplicate(candidate: TelegramUser, existing_people: list[tuple[str, str]]) -> bool:
    candidate_variants = {
        candidate.title,
        (candidate.first_name + " " + candidate.last_name).strip(),
        candidate.first_name.strip(),
        candidate.last_name.strip(),
    }
    candidate_variants = {item for item in candidate_variants if item}
    candidate_norms = {normalize(item) for item in candidate_variants if normalize(item)}
    candidate_tokens = set().union(*(tokenize(item) for item in candidate_variants))

    for first, last in existing_people:
        existing_full = (first + " " + last).strip()
        existing_variants = {existing_full, first.strip(), last.strip()}
        existing_variants = {item for item in existing_variants if item}
        existing_norms = {normalize(item) for item in existing_variants if normalize(item)}
        existing_tokens = set().union(*(tokenize(item) for item in existing_variants))
        if not existing_norms or not existing_tokens:
            continue
        if candidate_norms.intersection(existing_norms):
            return True
        if candidate_tokens and candidate_tokens.issubset(existing_tokens):
            return True
        if existing_tokens and existing_tokens.issubset(candidate_tokens):
            return True
    return False


def classify_job_title(user: TelegramUser) -> str:
    title = user.title.casefold()
    if any(token in title for token in SKIP_SUBSTRINGS):
        return "TG / personal"
    if user.mutual_contact or user.contact or user.phone:
        return "TG / contact"
    if any(token in title for token in ("broker", "finance", "invest", "manager", "office")):
        return "TG / business lead"
    return "TG / prospect"


def safe_snippet(text: str, limit: int = 260) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def build_note(user: TelegramUser) -> str:
    lines = [
        "Импорт из Telegram.",
        f"Диалог: {user.title}",
    ]
    if user.username:
        lines.append(f"Username: @{user.username}")
    if user.phone:
        lines.append(f"Phone: {user.phone}")
    lines.extend(
        [
            f"Mutual contact: {'yes' if user.mutual_contact else 'no'}",
            f"Contact: {'yes' if user.contact else 'no'}",
            f"Verified: {'yes' if user.verified else 'no'}",
            f"Premium: {'yes' if user.premium else 'no'}",
        ]
    )
    if user.last_date:
        lines.append(f"Last date: {user.last_date}")
    if user.last_message:
        lines.append(f"Last message: {safe_snippet(user.last_message)}")
    return "\n".join(lines)


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Import fresh Telegram dialogs into Twenty CRM.")
    parser.add_argument("--dry-run", action="store_true", help="Show candidates without writing to CRM.")
    args = parser.parse_args()

    users = load_telegram_users()
    existing_people = fetch_existing_people()

    candidates: list[TelegramUser] = []
    for user in users:
        title_lower = user.title.casefold()
        if not normalize(user.title):
            continue
        if title_lower in SKIP_TITLES:
            continue
        if any(skip in title_lower for skip in SKIP_SUBSTRINGS):
            continue
        if is_duplicate(user, existing_people):
            continue
        candidates.append(user)

    print(f"Telegram users: {len(users)}")
    print(f"Existing CRM people: {len(existing_people)}")
    print(f"New CRM candidates: {len(candidates)}")
    for item in candidates:
        print(f"  + {item.title}")

    if args.dry_run or not candidates:
        return

    sql_lines = ["BEGIN;"]
    for user in candidates:
        person_id = str(uuid4())
        note_id = str(uuid4())

        display_name = user.title or (user.first_name + " " + user.last_name).strip() or user.username or user.phone or "Telegram contact"
        first_name = clean_name(user.first_name or display_name)
        last_name = clean_name(user.last_name if user.first_name else "")
        job_title = classify_job_title(user)
        note_body = build_note(user).replace("'", "''")

        sql_lines.append(
            f"""
INSERT INTO {SCHEMA}.person (
  id, "nameFirstName", "nameLastName", "jobTitle",
  "createdBySource", "createdByName", "updatedBySource", "updatedByName"
) VALUES (
  '{person_id}', '{first_name.replace("'", "''")}', NULLIF('{last_name.replace("'", "''")}', ''),
  '{job_title.replace("'", "''")}', 'MANUAL', '{CREATED_BY}', 'MANUAL', '{CREATED_BY}'
);
"""
        )
        sql_lines.append(
            f"""
INSERT INTO {SCHEMA}."note" (
  id, title, "bodyV2Markdown",
  "createdBySource", "createdByName", "updatedBySource", "updatedByName"
) VALUES (
  '{note_id}', 'Telegram import', '{note_body}',
  'MANUAL', '{CREATED_BY}', 'MANUAL', '{CREATED_BY}'
);

INSERT INTO {SCHEMA}."noteTarget" ("noteId", "targetPersonId")
VALUES ('{note_id}', '{person_id}');
"""
        )

    sql_lines.append("COMMIT;")
    output = psql("\n".join(sql_lines))
    print(output)


if __name__ == "__main__":
    main()
