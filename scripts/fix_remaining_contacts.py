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
    output = result.stdout.decode("utf-8", errors="replace")
    print(output)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> None:
    sql = dedent(
        f"""
        BEGIN;

        UPDATE {SCHEMA}."note" SET title = 'Контекст по лиду из чата', "bodyV2Markdown" = 'Теплый лид из общего чата. Нужно проверить интерес и понять, есть ли окно на повторный контакт.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '901e77a9-819c-4bb9-90bb-366927daf6bf';
        UPDATE {SCHEMA}."task" SET title = 'Проверить лид из чата', "bodyV2Markdown" = 'Понять, жив ли контакт и есть ли смысл возвращаться к ARM.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = 'e44cb299-25fd-4873-837d-fd38cfc83cf7';

        UPDATE {SCHEMA}."note" SET title = 'Контекст по Артему', "bodyV2Markdown" = 'Теплый контакт, был интерес к ARM и к продолжению диалога. Можно мягко поднимать на повторный контакт.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = 'a1bed8a4-bd5a-4ef4-a4c7-bf0b81d1f886';
        UPDATE {SCHEMA}."task" SET title = 'Проверить Артема', "bodyV2Markdown" = 'Проверить, актуален ли контакт и стоит ли возвращать его в диалог.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '952f4f70-f541-447e-aad9-3364b9f44a04';

        UPDATE {SCHEMA}."note" SET title = 'Контекст по Парфену', "bodyV2Markdown" = 'Интересовался ARM и конференцией. Контакт не закрыт, можно аккуратно возвращать в разговор.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '8c732df7-c59c-4211-8981-b0d195995ec0';
        UPDATE {SCHEMA}."task" SET title = 'Проверить Парфена', "bodyV2Markdown" = 'Уточнить, есть ли смысл возвращать его в диалог и на чем строить следующий шаг.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '338f001c-dc5d-425a-b218-62e4f3da2760';

        UPDATE {SCHEMA}."note" SET title = 'Контекст по Пичугину', "bodyV2Markdown" = 'Максимальный тариф подключен, партнерский потенциал есть, но сейчас осторожничает из-за стагнации. Нужен мягкий follow-up.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '7b77773f-442a-4afe-8034-22e93d04834a';
        UPDATE {SCHEMA}."task" SET title = 'Проверить Пичугина', "bodyV2Markdown" = 'Проверить, готов ли он снова обсуждать партнерку или пополнение.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = 'cd42cc22-9f65-4397-a847-5b86e6f17b7c';

        UPDATE {SCHEMA}."note" SET title = 'Контекст по Alex fx', "bodyV2Markdown" = 'Партнер в другой ветке, не клиент. Держать связь, но не перегружать прямыми продажами.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '48c04d69-a79f-4004-878c-51361562608d';
        UPDATE {SCHEMA}."task" SET title = 'Проверить Alex fx', "bodyV2Markdown" = 'Проверить, есть ли у него что-то по партнерской линии или новым контактам.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '353ebf54-3cdb-4639-af0a-a9581ae942dc';

        UPDATE {SCHEMA}."note" SET title = 'Контекст по Anne', "bodyV2Markdown" = 'Сейчас на паузе, работает сама по себе. Возвращаться только если появится реальный повод.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '2aa258f0-943e-4060-af47-82ecdc8a9a71';
        UPDATE {SCHEMA}."task" SET title = 'Проверить Anne', "bodyV2Markdown" = 'Не форсировать, просто проверить наличие окна на контакт.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '1137977a-d84d-4939-90cf-63f4ca538564';

        UPDATE {SCHEMA}."note" SET title = 'Контекст по Anton Merkulov', "bodyV2Markdown" = 'Менеджер брокера, не клиент. Полезен как рабочий контакт по площадке и источнику информации.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = 'cfd0f0a8-da4c-4094-a0ec-442d427c51e3';
        UPDATE {SCHEMA}."task" SET title = 'Проверить Anton Merkulov', "bodyV2Markdown" = 'Не продавать в лоб, а держать как рабочий контакт по брокеру.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = 'f426ac0a-3958-4018-a0f2-eac993c5f39b';

        UPDATE {SCHEMA}."note" SET title = 'Контекст по Blitz', "bodyV2Markdown" = 'Продает рекламу. Не прямой инвестор, но полезен как медийный и партнерский контакт.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '542d5af4-43b0-4c87-b7e2-d51e3fb4524b';
        UPDATE {SCHEMA}."task" SET title = 'Проверить Blitz', "bodyV2Markdown" = 'Проверить, можно ли использовать его как медийный или партнерский контакт.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = 'f5537a6c-bb37-4248-a169-6ed50b1c8adf';

        UPDATE {SCHEMA}."note" SET title = 'Контекст по Duff', "bodyV2Markdown" = 'Конференционный лид. Можно возвращать к теме ARM и смотреть, есть ли окно на продолжение диалога.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = 'c8b5d4e8-a137-4a41-aa03-40193aff2a70';
        UPDATE {SCHEMA}."task" SET title = 'Проверить Duff', "bodyV2Markdown" = 'Проверить, не потерян ли контакт и стоит ли продолжать follow-up.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = 'f1261d73-40de-4e1b-bf72-6ed45067c20a';

        UPDATE {SCHEMA}."note" SET title = 'Контекст по Evgenii Afanasev', "bodyV2Markdown" = 'Лид с конференции. Интересовался ARM и потенциальным развитием, можно мягко возвращать к разговору.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = 'ba47a6fa-b659-46e6-b510-b9984b79f590';
        UPDATE {SCHEMA}."task" SET title = 'Вернуть Evgenii Afanasev в диалог', "bodyV2Markdown" = 'Проверить, есть ли окно на повторный контакт после конференции.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '2693289c-478d-447c-b848-bfd60bba712b';

        UPDATE {SCHEMA}."note" SET title = 'Контекст по Mody', "bodyV2Markdown" = 'Лид из конференции. Сначала проверить интерес, потом выводить на следующий шаг по ARM.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '6d689911-898b-4140-9529-e0dde593a560';
        UPDATE {SCHEMA}."task" SET title = 'Проверить Mody', "bodyV2Markdown" = 'Посмотреть, можно ли его мягко вернуть в диалог.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = 'c690aebb-0134-4cb7-9e04-a878bba81a42';

        UPDATE {SCHEMA}."note" SET title = 'Контекст по Алексею Сагирову', "bodyV2Markdown" = 'Интересовался кейсом и видео по ARM. Контакт теплый, можно продолжать дожимать через кейс и созвон.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '1d059dac-5a48-4b9e-a0ca-cd0a7e32728c';
        UPDATE {SCHEMA}."task" SET title = 'Проверить ответ Алексея Сагирова', "bodyV2Markdown" = 'Следить за реакцией на видео-кейс и вернуть к обсуждению подключения.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '118299cb-1d0b-4e6d-b148-d7b54854a99e';

        UPDATE {SCHEMA}."note" SET title = 'Контекст по Андрею Меренкову', "bodyV2Markdown" = 'Был интерес к ARM, но контакт давно стоит. Возвращать только мягко и с коротким сообщением.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '7d9df9d8-2e5d-4bb2-b33c-8f8c90b2ce6e';
        UPDATE {SCHEMA}."task" SET title = 'Повторный выход к Андрею Меренкову', "bodyV2Markdown" = 'Проверить, есть ли окно на продолжение диалога и следующее касание.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '9dee26c7-9a2e-41a6-9b63-6b2af0c6167e';

        UPDATE {SCHEMA}."note" SET title = 'Контекст по Анне', "bodyV2Markdown" = 'Сейчас на паузе. При появлении повода можно мягко вернуть в контакт.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '13af1df7-8d58-4fa5-9b75-41b3ea990161';
        UPDATE {SCHEMA}."task" SET title = 'Проверить Анну', "bodyV2Markdown" = 'Проверить, не появился ли у нее повод вернуться к разговору.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = 'f085f548-e03e-4052-aaad-ba409287495d';

        UPDATE {SCHEMA}."note" SET title = 'Контекст по Виктору Коневу', "bodyV2Markdown" = 'Интересный контакт, уже есть встреча и обсуждение следующего шага. Его нужно держать в работе.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = 'f56482f3-aa8a-4bd0-a365-86466425bdfc';
        UPDATE {SCHEMA}."task" SET title = 'Собрать итог по Виктору Коневу', "bodyV2Markdown" = 'Зафиксировать, что он уже работает с нами и что нужно делать дальше по встрече и подключению.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '7bfa2281-7a18-4e4d-bfb1-a650605d5b30';

        UPDATE {SCHEMA}."note" SET title = 'Контекст по Денису Боровику', "bodyV2Markdown" = 'Старый лид, в настоящий момент не дает явного сигнала. Нужен очень мягкий follow-up.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = 'c2e87c99-25d8-4fd4-84f0-1656176f4334';
        UPDATE {SCHEMA}."task" SET title = 'Проверить Дениса Боровика', "bodyV2Markdown" = 'Осторожный старый лид, без давления понять, есть ли смысл возвращать в диалог.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '381b06ef-bb4c-4e4f-8bc1-6ee601072a81';

        UPDATE {SCHEMA}."note" SET title = 'Контекст по Дмитрию Жестереву', "bodyV2Markdown" = 'Инвестор с минимальным депозитом, постоянно говорит, что денег нет. Контакт живой, но сейчас без движения.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '49ace965-47b6-4134-bba0-5fc0795fece0';
        UPDATE {SCHEMA}."task" SET title = 'Проверить Дмитрия Жестерева', "bodyV2Markdown" = 'Проверить, есть ли новый повод вернуться к контакту, но без ожидания быстрого результата.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '025c02fb-1f14-464f-bc4a-024ab65b0968';

        UPDATE {SCHEMA}."note" SET title = 'Контекст по Ларисе Гришиной', "bodyV2Markdown" = 'Бывший партнер, сейчас в сторонних историях. Контакт держать, но без лишнего давления.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '78b051a0-526e-483a-916e-54a06cc6629a';
        UPDATE {SCHEMA}."task" SET title = 'Проверить Ларису Гришину', "bodyV2Markdown" = 'Проверить, можно ли вернуть ее в рабочий партнерский контур или она окончательно в паузе.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '81c20b5f-ea5d-46f2-a512-e713875f2594';

        UPDATE {SCHEMA}."note" SET title = 'Контекст по Левику', "bodyV2Markdown" = 'Пропал из поля зрения, но у него есть потенциал для работы. Его можно проверять на возвращение.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '35421baa-f471-4d19-adf9-01c4b7932307';
        UPDATE {SCHEMA}."task" SET title = 'Проверить Левика', "bodyV2Markdown" = 'Давний контакт, проверить, не появился ли у него повод снова выйти на связь.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '1b5e3efb-5351-4731-8aa8-a109b5c268fe';

        UPDATE {SCHEMA}."note" SET title = 'Контекст по Лене', "bodyV2Markdown" = 'Давний контакт, уже брал деньги. Сейчас лучше работать точечно и без перегрева.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = 'd1c6b1fe-d4a5-4978-81ba-787e00edbbd7';
        UPDATE {SCHEMA}."task" SET title = 'Проверить Лену', "bodyV2Markdown" = 'Спокойно проверить, есть ли повод писать и нет ли у нее нового окна.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = 'a4632da3-b92e-4741-b0e2-b336ee8fd2b4';

        UPDATE {SCHEMA}."note" SET title = 'Контекст по Олегу Уткину', "bodyV2Markdown" = 'Был интерес к ARM, потом пауза. Контакт можно возвращать после удобного окна.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '12b9659d-0b3e-48b2-a351-66b8c9742867';
        UPDATE {SCHEMA}."task" SET title = 'Проверить окно для Олега Уткина', "bodyV2Markdown" = 'Понять, есть ли сейчас смысл выходить с follow-up по ARM и партнерке.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '6501d56f-d111-4044-886d-9649007e9ec0';

        UPDATE {SCHEMA}."note" SET title = 'Контекст по Рамзе', "bodyV2Markdown" = 'Ушел в паузу и сейчас не движется. Можно рассматривать как старый lead, если появится хороший повод.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '71388994-f9dd-4e5e-a6a5-2e70ccb90959';
        UPDATE {SCHEMA}."task" SET title = 'Проверить Рамзу', "bodyV2Markdown" = 'Проверить, можно ли его снова возвращать в диалог, но ожидать осторожную реакцию.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '3222fbcf-32a1-4121-9168-c7290da541df';

        UPDATE {SCHEMA}."note" SET title = 'Контекст по Степану', "bodyV2Markdown" = 'Есть потенциальный интерес, но он давно не активен. Нужно аккуратно проверять окно на контакт.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = '25ba42f7-9d24-4ae0-bda6-bd9ef9d91e33';
        UPDATE {SCHEMA}."task" SET title = 'Вернуть Степана в диалог', "bodyV2Markdown" = 'Проверить, не потерялся ли он, и мягко вернуть в контакт без формального захода.', "updatedByName" = 'Alexandr RYZHKOV' WHERE id = 'b61357a9-d8a9-453f-b0e0-3e22b133013d';

        COMMIT;
        """
    ).strip()
    run_sql(sql)


if __name__ == "__main__":
    main()
