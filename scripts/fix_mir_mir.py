import subprocess

SCHEMA = "workspace_aqgjkvzyjiktitsgg1e0evek1"
PERSON_ID = "2f6aeb84-c314-44bd-b5a0-1446d6a8ac42"


def main() -> None:
    sql = f"""
BEGIN;
UPDATE {SCHEMA}.person
SET
  "nameFirstName" = 'Мир',
  "nameLastName" = 'Мир',
  "jobTitle" = 'ARM / investor + partner',
  "updatedByName" = 'Alexandr RYZHKOV'
WHERE id = '{PERSON_ID}';

UPDATE {SCHEMA}."note" n
SET
  title = 'Контекст по возврату',
  "bodyV2Markdown" = 'Сказал, что хочет вернуться и закинуть 10k USD на счет. Контакт теплый, держать в работе до пополнения и не терять окно.',
  "updatedByName" = 'Alexandr RYZHKOV'
FROM {SCHEMA}."noteTarget" nt
WHERE nt."noteId" = n.id
  AND nt."targetPersonId" = '{PERSON_ID}';

UPDATE {SCHEMA}."task" t
SET
  title = 'Довести до пополнения',
  "bodyV2Markdown" = 'Коротко вернуть в диалог, довести до пополнения на счет и зафиксировать следующий шаг.',
  "updatedByName" = 'Alexandr RYZHKOV'
FROM {SCHEMA}."taskTarget" tt
WHERE tt."taskId" = t.id
  AND tt."targetPersonId" = '{PERSON_ID}';
COMMIT;
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
        ],
        input=sql.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(result.stdout.decode("utf-8", errors="replace"))


if __name__ == "__main__":
    main()
