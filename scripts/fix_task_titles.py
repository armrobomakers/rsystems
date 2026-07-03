import subprocess

SCHEMA = "workspace_aqgjkvzyjiktitsgg1e0evek1"

UPDATES = [
    ("80542949-89be-442c-abfe-d188fdaa162e", "Проверить окно для Олега Уткина"),
    ("576986a3-d5a8-484e-8648-444fcdc6eba1", "Проверить ответ Игоря Волынкина"),
    ("4bbb3385-84e6-4b10-9900-7cddf5be8fcf", "Созвон с Евгением Доброделом"),
    ("0a187084-36ec-4a43-8b15-a5c4f8f257ef", "Дожать контакт Виталия Ермоленко"),
    ("4d2dd9a6-ceed-4e33-8bb4-b2480fb8b69a", "Повторный выход к Андрею Меренкову"),
    ("9b31ae9b-e499-408a-96c4-3e834be35d0c", "Проверить ответ Алексея Сагирова"),
    ("31af43a8-2d6d-4653-8525-41cd0f1f5178", "Вернуть Марка Колесникова в диалог"),
    ("72d27f74-08aa-4cf2-8378-00a721c64e5b", "Проверить Дениса Боровика"),
    ("bc7558af-70eb-4b4c-86ee-a262ef1978d9", "Вернуть Сергея Борисова в диалог"),
    ("640ece23-8524-4171-b704-755409822b20", "Дожать Владимира Скаредина"),
    ("2719c23a-a701-43f0-8c22-97d7c13a8e67", "Проверить Вячеслава"),
    ("702f946b-e22a-4753-94c2-074660adb605", "Собрать итог по Виктору Коневу"),
    ("242dc732-a1e6-4389-b021-f172cc363a0b", "Возобновить диалог с Романом Демидовым"),
    ("3c9aba8b-aa7a-4202-a9b9-e0e1432cf59f", "Проверить Дмитрия Жестерева"),
    ("4879774f-294d-44d9-83eb-e4649ab5d442", "Подготовить следующий шаг для Ирен"),
    ("116bb509-555a-4235-b4d7-e201477bb5da", "Вернуть Степана в диалог"),
    ("5b83cbbf-ec7b-4aa5-90a9-45012a40b0e3", "Проверить Олега Сидорова"),
    ("00cad869-612b-4b11-b2ce-64013444517a", "Вернуть МирМир в диалог"),
    ("1a540f41-1090-4bb8-93ef-df3ad9073335", "Актуализировать Пичугина"),
    ("fa9d945b-92dd-4441-a0a8-663ddf13fc7d", "Поднять Курбатова"),
    ("18ba1f60-e1b2-4028-abe2-7e7c3ab28695", "Проверить Левика"),
    ("2a58caf4-5753-4951-807c-f616e94399ee", "Проверить Ракова"),
    ("11b0bb98-ac57-4ae1-b1bd-4a548dcbdc8f", "Проверить Карпенко"),
    ("81c81a56-9955-41f8-bedb-2a86aa556277", "Проверить Duff"),
    ("f7222875-388e-49ce-9bae-54a156a27749", "Проверить Mody"),
    ("6af48c12-cf89-45de-878a-6a01fe701d2a", "Проверить Парфена"),
    ("8d392ee1-3dd3-4e3f-abe7-843bf2d2a9b5", "Вернуть Evgenii Afanasev в диалог"),
    ("50383ba1-168d-4c44-b008-10f838b26886", "Проверить Артема"),
    ("c4221bae-8803-45dc-b210-c289c5b7bf33", "Проверить Игоря из лидов"),
    ("72bd5003-13ec-45d2-ba56-969adc33655e", "Проверить D S"),
    ("25d7b556-3129-4cf5-a2c4-dbdc6bc569ce", "Проверить Anne"),
    ("aa245628-f0e1-41bb-a59b-cc9ae964f5c7", "Проверить Blitz"),
    ("618e33cd-de7e-44cc-a292-bd1ee7f864a3", "Проверить Alex fx"),
    ("109ca174-4f48-4f96-a386-e9cafdc11184", "Проверить Пичугина"),
    ("9be4ed4a-4af4-4ce5-99e7-c6b270db8e43", "Проверить Саню"),
    ("e46b4a87-5128-4afb-86f1-c91f1f0a18ce", "Проверить Anton Merkulov"),
    ("d289b0fd-35a8-48d4-bbe2-2d06477789f5", "Проверить Ларису Гришину"),
    ("d68e9228-f689-4445-bb74-0717da56a0d8", "Проверить Лену"),
    ("0e4fbc3b-a16d-43b6-afdb-9abb4c60edfe", "Проверить Анну"),
    ("6ca7b7d0-2a75-4bce-ae40-e38617d5ca47", "Проверить Рамзу"),
]


def main() -> None:
    sql_parts = ["BEGIN;"]
    for person_id, title in UPDATES:
        safe_title = title.replace("'", "''")
        sql_parts.append(
            f"UPDATE {SCHEMA}.\"task\" t "
            f"SET title = '{safe_title}', "
            f"\"updatedByName\" = 'Alexandr RYZHKOV' "
            f"FROM {SCHEMA}.\"taskTarget\" tt "
            f"WHERE tt.\"taskId\" = t.id AND tt.\"targetPersonId\" = '{person_id}';"
        )
    sql_parts.append("COMMIT;")
    sql = "\n".join(sql_parts) + "\n"

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
