from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCHEMA = "workspace_aqgjkvzyjiktitsgg1e0evek1"
OUT_PATH = ROOT / "outputs" / "reality_brief.md"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


@dataclass
class TaskRow:
    title: str
    due_at: datetime | None
    target: str


@dataclass
class PersonRow:
    name: str
    job_title: str
    updated_at: datetime | None
    priority: int


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


def parse_dt(raw: str) -> datetime | None:
    raw = (raw or "").strip()
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def clean_text(text: str) -> str:
    return " ".join((text or "").split()).strip()


def load_tasks() -> list[TaskRow]:
    sql = f"""
        SELECT DISTINCT ON (t.id)
               coalesce(t.title, '') AS title,
               coalesce(t."dueAt"::text, '') AS due_at,
               coalesce(
                 nullif(trim(coalesce(p."nameFirstName", '') || ' ' || coalesce(p."nameLastName", '')), ''),
                 ''
               ) AS target
        FROM {SCHEMA}.task t
        LEFT JOIN {SCHEMA}."taskTarget" tt
          ON tt."taskId" = t.id
         AND tt."deletedAt" IS NULL
        LEFT JOIN {SCHEMA}.person p
          ON p.id = tt."targetPersonId"
        WHERE t."deletedAt" IS NULL
          AND t.status = 'TODO'
        ORDER BY t.id, tt."createdAt" NULLS LAST;
    """
    rows: list[TaskRow] = []
    for line in psql(sql).splitlines():
        if not line.strip():
            continue
        title, due_at, target = (line.split("\t") + ["", "", ""])[:3]
        rows.append(TaskRow(clean_text(title), parse_dt(due_at), clean_text(target)))
    return rows


def load_people() -> list[PersonRow]:
    sql = f"""
        SELECT coalesce("nameFirstName", '') AS first_name,
               coalesce("nameLastName", '') AS last_name,
               coalesce("jobTitle", '') AS job_title,
               coalesce("updatedAt"::text, '') AS updated_at
        FROM {SCHEMA}.person
        WHERE "deletedAt" IS NULL
        ORDER BY "updatedAt" DESC, "createdAt" DESC;
    """
    rows: list[PersonRow] = []
    for line in psql(sql).splitlines():
        if not line.strip():
            continue
        first, last, job, updated = (line.split("\t") + ["", "", "", ""])[:4]
        name = clean_text(f"{first} {last}")
        job_title = clean_text(job)
        priority = score_person(job_title)
        rows.append(PersonRow(name or clean_text(first) or "Без имени", job_title, parse_dt(updated), priority))
    return rows


def score_person(job_title: str) -> int:
    text = job_title.casefold()
    score = 0
    if "investor" in text or "инвестор" in text:
        score += 50
    if "partner" in text or "партнер" in text:
        score += 45
    if "lead" in text or "лид" in text:
        score += 35
    if "warm" in text or "тёпл" in text or "тепл" in text:
        score += 25
    if "dormant" in text or "спящ" in text:
        score += 20
    if "contact" in text or "контакт" in text:
        score += 15
    if "negative" in text or "негатив" in text or "do-not-touch" in text:
        score -= 60
    if "internal" in text or "сотрудник" in text or "manager" in text:
        score -= 20
    return score


def format_dt(dt: datetime | None) -> str:
    if not dt:
        return "-"
    return dt.astimezone().strftime("%d.%m %H:%M")


def main() -> None:
    today = date.today()
    tasks = load_tasks()
    people = load_people()

    due_now = []
    next_up = []
    for task in tasks:
        if task.due_at is None:
            next_up.append(task)
            continue
        due_date = task.due_at.astimezone().date()
        if due_date <= today:
            due_now.append(task)
        else:
            next_up.append(task)

    due_now.sort(key=lambda item: (item.due_at or datetime.max))
    next_up.sort(key=lambda item: (item.due_at or datetime.max))
    people = [person for person in people if person.priority != 0]
    people.sort(key=lambda item: (-item.priority, item.updated_at or datetime.min), reverse=False)
    people.sort(key=lambda item: (-item.priority, item.updated_at or datetime.min), reverse=False)
    people = sorted(people, key=lambda item: (-item.priority, -(item.updated_at.timestamp() if item.updated_at else 0)))

    lines = [
        "# Reality Brief",
        f"- Date: {today.isoformat()}",
        f"- Open tasks: {len(tasks)}",
        f"- Urgent tasks: {len(due_now)}",
        f"- High-priority contacts: {len(people)}",
        "",
        "## First 3 actions",
    ]

    top_actions = due_now[:3] if due_now else next_up[:3]
    for idx, task in enumerate(top_actions, 1):
        target = f" -> {task.target}" if task.target else ""
        due = f" [due {format_dt(task.due_at)}]" if task.due_at else ""
        lines.append(f"{idx}. {task.title}{target}{due}")

    lines.extend([
        "",
        "## Tasks now",
    ])
    for task in due_now[:12]:
        target = f" -> {task.target}" if task.target else ""
        due = f" [due {format_dt(task.due_at)}]" if task.due_at else ""
        lines.append(f"- {task.title}{target}{due}")

    lines.extend([
        "",
        "## Next up",
    ])
    for task in next_up[:12]:
        target = f" -> {task.target}" if task.target else ""
        due = f" [due {format_dt(task.due_at)}]" if task.due_at else ""
        lines.append(f"- {task.title}{target}{due}")

    lines.extend([
        "",
        "## Contacts to touch",
    ])
    for person in people[:15]:
        extra = f" ({person.job_title})" if person.job_title else ""
        updated = f" updated {format_dt(person.updated_at)}" if person.updated_at else ""
        lines.append(f"- {person.name}{extra}{updated}")

    lines.extend([
        "",
        "## Rule",
        "- Finish one task before opening a new thread.",
        "- If a contact has no next action, assign one or move on.",
        "- Keep the focus on money, pipeline, and follow-up only.",
    ])

    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(OUT_PATH)
    print(f"Due now: {len(due_now)}")
    print(f"Next up: {len(next_up)}")
    for line in lines[:20]:
        print(line)


if __name__ == "__main__":
    main()
