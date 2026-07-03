import subprocess
from textwrap import dedent

SCHEMA = "workspace_aqgjkvzyjiktitsgg1e0evek1"


def run_sql(sql: str) -> None:
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
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> None:
    sql = dedent(
        f"""
        BEGIN;

        UPDATE {SCHEMA}.person
        SET
          "nameFirstName" = 'Пичугин',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '109ca174-4f48-4f96-a386-e9cafdc11184';

        UPDATE {SCHEMA}.person
        SET
          "nameFirstName" = 'Артем',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '50383ba1-168d-4c44-b008-10f838b26886';

        UPDATE {SCHEMA}.person
        SET
          "nameFirstName" = 'Парфен',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '6af48c12-cf89-45de-878a-6a01fe701d2a';

        UPDATE {SCHEMA}.person
        SET
          "nameFirstName" = 'Лид из чата',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = 'c4221bae-8803-45dc-b210-c289c5b7bf33';

        COMMIT;
        """
    ).strip()
    run_sql(sql)


if __name__ == "__main__":
    main()
