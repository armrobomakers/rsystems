from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "outputs" / "telegram_archive_groups" / "_index.json"
OUT_JSON = ROOT / "outputs" / "telegram_groups_classified.json"
OUT_MD = ROOT / "outputs" / "telegram_groups_report.md"

RULES = [
    ("personal", ["семья", "мысли идеи планы", "инстаграм финансы", "ryzhkov", "today"]),
    ("arm", ["arm", "робо", "algo", "algofox", "pamm", "tickmill", "hedgecore", "роботы", "пассивного дохода"]),
    ("soulmate", ["soulmate", "нейро", "амбассадоры soulmate", "команда soulmate", "бизнес soulmate", "инвест среда soulmate"]),
    ("trading", ["forex", "mql5", "broker", "finance", "trade", "investing.com", "invest", "крипт", "capital", "fincult", "rannforex", "smartforex", "cifra"]),
    ("local", ["екатеринбург", "екб", "москва", "казань", "перм", "уфа", "самара", "новосибирск", "ростов", "челябинск", "омск", "волгоград", "красноярск", "санкт-петербург"]),
    ("community", ["чат", "канал", "community", "club", "team", "сообщество", "конференц", "бизнес", "задоя", "маргулан"]),
]


def classify(title: str) -> str:
    low = title.casefold()
    for category, keywords in RULES:
        if any(keyword in low for keyword in keywords):
            return category
    return "other"


def main() -> None:
    if not INDEX_PATH.exists():
        raise SystemExit(f"Missing archive index: {INDEX_PATH}")

    rows = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    classified = []
    for row in rows:
        item = dict(row)
        item["category"] = classify(item.get("title", ""))
        classified.append(item)

    OUT_JSON.write_text(json.dumps(classified, ensure_ascii=False, indent=2), encoding="utf-8")

    counts = Counter(item["category"] for item in classified)
    useful = [item for item in classified if item["category"] != "other"]
    useful.sort(key=lambda item: (-item.get("messageCount", 0), item["title"]))

    lines = [
        "# Telegram Group Archive",
        "",
        "## Counts",
    ]
    for category, count in sorted(counts.items(), key=lambda item: (item[0], item[1])):
        lines.append(f"- {category}: {count}")

    lines.extend([
        "",
        "## Useful Groups",
    ])
    for item in useful[:80]:
        lines.append(f"- [{item['category']}] {item.get('messageCount', 0):>3} {item.get('title', '')}")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print("Counts:")
    for category, count in sorted(counts.items(), key=lambda item: (item[0], item[1])):
        print(f"  {category}: {count}")


if __name__ == "__main__":
    main()
