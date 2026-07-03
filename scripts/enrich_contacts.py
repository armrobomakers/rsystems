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

        UPDATE {SCHEMA}."note"
        SET
          title = 'Контекст по D S',
          "bodyV2Markdown" = 'Банки не пропускают из-за риска и СБ. Ранее обсуждали Цифра Брокер и Freedom Finance. Контакт живой, но уперся в банковский блок. Следующий шаг: держать в работе и возвращаться к теме только при появлении легального рабочего варианта.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '05b3f117-8e6c-47d2-8fae-6441ddda870f';

        UPDATE {SCHEMA}."task"
        SET
          title = 'Проверить D S',
          "bodyV2Markdown" = 'Проверить свежий статус по банкам и зафиксировать, есть ли легальный рабочий маршрут.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '42f39db7-26b3-4aac-b793-882f59a8381b';

        UPDATE {SCHEMA}."note"
        SET
          title = 'Партнерский контекст Евгения Добродела',
          "bodyV2Markdown" = 'Партнер компании, привлекает инвесторов в robomakers.org. Мотивация: 35% от продаж и 15% от чистой прибыли компании. Контакт теплый, задача — мягко реанимировать и перевести в созвон.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '76dbacba-cd12-4305-b473-944411f04ecd';

        UPDATE {SCHEMA}."task"
        SET
          title = 'Вернуть Евгения Добродела в диалог',
          "bodyV2Markdown" = 'Сделать короткий follow-up, без давления, и дожать до созвона по партнерке.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = 'ee1e478d-5fe9-4723-8790-0c59fa09bf0a';

        UPDATE {SCHEMA}."task"
        SET
          title = 'Созвон с Евгением Доброделом',
          "bodyV2Markdown" = 'Сначала актуализировать, потом выйти на созвон и проговорить вход в партнерский трек.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '6d2f59d1-ab19-428f-bd96-7eebdc89b96b';

        UPDATE {SCHEMA}."note"
        SET
          title = 'Офисная встреча и партнерский потенциал',
          "bodyV2Markdown" = 'Вернется в офис 2 июля в 14:00. Контакт теплый, есть смысл проговорить подключение и партнерский потенциал лично.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = 'da7055a6-facf-42b2-af5d-76e6c426ba34';

        UPDATE {SCHEMA}."task"
        SET
          title = 'Встреча со Скарединым в офисе',
          "bodyV2Markdown" = 'Встретить в офисе 2 июля в 14:00, обсудить подключение и зафиксировать следующий шаг.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '0317e23d-dac2-4143-bc66-dac20fd95b7c';

        UPDATE {SCHEMA}."note"
        SET
          title = 'ARM и следующий шаг по Сергею Борисову',
          "bodyV2Markdown" = 'Обсуждали ARM, видеокейс и следующий шаг после просмотра. Контакт теплый, уже в диалоге по инвестиции и партнерству.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '2d9dfb6a-fed6-49ff-9800-e69718151157';

        UPDATE {SCHEMA}."task"
        SET
          title = 'Вернуть Сергея Борисова в диалог',
          "bodyV2Markdown" = 'Коротко поднять тему видео и кейса и вывести на следующий созвон без лишнего текста.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = 'cb686887-eba5-44f3-8c7f-81ba088cafd6';

        UPDATE {SCHEMA}."note"
        SET
          title = 'ARM follow-up по Игорю Волынкину',
          "bodyV2Markdown" = 'В переписке были вопросы по Tickmill и дальнейшему движению. Контакт живой, можно возвращаться к ARM и партнерке по follow-up.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = 'e3302f42-c422-488e-92e4-5ec9347f5668';

        UPDATE {SCHEMA}."task"
        SET
          title = 'Проверить окно для Игоря Волынкина',
          "bodyV2Markdown" = 'Вернуться к ARM и посмотреть, готов ли он к следующему шагу.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '032a4f78-cffb-486d-a955-a3894928d2a1';

        UPDATE {SCHEMA}."task"
        SET
          title = 'Follow-up по Игорю Волынкину',
          "bodyV2Markdown" = 'Проверить ответ и, если окно есть, вывести на созвон.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '55cc77d6-ed23-420e-bc8e-db8b4a8f2c5c';

        UPDATE {SCHEMA}."note"
        SET
          title = 'Контекст по возврату',
          "bodyV2Markdown" = 'Сказал, что хочет вернуться и закинуть 10k USD на счет. Потенциал на пополнение и партнерку, контакт держать живым.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '322a6bfb-4ad7-4981-89c0-9fd3c69aefde';

        UPDATE {SCHEMA}."task"
        SET
          title = 'Довести до пополнения',
          "bodyV2Markdown" = 'Вернуть в диалог, не отпускать до пополнения, потом проверить партнерский трек.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '4e278f43-e885-4eb0-b53a-455f19b0e99f';

        UPDATE {SCHEMA}."note"
        SET
          title = 'Партнерский контекст Виталия Ермоленко',
          "bodyV2Markdown" = 'Клиент и партнер. Контакт живой, можно развивать через партнерку и follow-up по встрече и инфе.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = 'd155bcfe-b7dd-4977-a857-f67d694717fd';

        UPDATE {SCHEMA}."task"
        SET
          title = 'Дожать контакт Виталия Ермоленко',
          "bodyV2Markdown" = 'Проверить, готов ли он к следующему шагу по партнерке и не потерять контакт.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = 'e31de09e-2776-41b7-b305-c6cd886ba5bf';

        UPDATE {SCHEMA}."note"
        SET
          title = 'Потенциал по Вячеславу',
          "bodyV2Markdown" = 'Хороший старый контакт, есть сеть и потенциальный партнерский потенциал. Нужен мягкий follow-up и проверка его окружения.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = 'ecb40dea-a111-438f-9d48-001bc3e1df08';

        UPDATE {SCHEMA}."task"
        SET
          title = 'Проверить Вячеслава',
          "bodyV2Markdown" = 'Проверить окно на созвон и понять, можно ли расшевелить контакт.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '4342111e-764d-434c-8375-03296da70bfd';

        UPDATE {SCHEMA}."note"
        SET
          title = 'Партнерский потенциал Ирен',
          "bodyV2Markdown" = 'Сначала приветствие и короткий контакт, потом аккуратно спрашивать про инвестицию и людей для привлечения. Давить не надо.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '42c72145-8aff-4e47-a932-204606f47b6f';

        UPDATE {SCHEMA}."task"
        SET
          title = 'Подготовить следующий шаг для Ирен',
          "bodyV2Markdown" = 'Подготовить мягкий follow-up и не форсировать, пока не появится окно.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '547f4a29-9337-4ce7-a09d-84d2186173ba';

        UPDATE {SCHEMA}."note"
        SET
          title = 'Контекст по Карпенко',
          "bodyV2Markdown" = 'Спящий инвестор, ждет прибыль по ARM. Сейчас на паузе, но контакт может вернуться после улучшения результата.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '6467c4b1-5cf7-49b0-bdf8-a7424bac7312';

        UPDATE {SCHEMA}."task"
        SET
          title = 'Проверить Карпенко',
          "bodyV2Markdown" = 'Проверить, появился ли повод вернуть его в диалог.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = 'cdd7ff0a-d733-456d-b344-126581e5abb6';

        UPDATE {SCHEMA}."note"
        SET
          title = 'Потенциал Курбатова',
          "bodyV2Markdown" = 'Может приводить людей, потенциал по партнерке есть. Его стоит аккуратно разогревать и выводить на обсуждение контактов.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '861fae64-18d8-4705-bcc0-6b179142d863';

        UPDATE {SCHEMA}."task"
        SET
          title = 'Поднять Курбатова',
          "bodyV2Markdown" = 'Поднять контакт и проверить, есть ли у него люди или рефералы.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '4713a23f-2c29-4e40-874c-e5e17bae8c53';

        UPDATE {SCHEMA}."note"
        SET
          title = 'Партнерский контекст Марка Колесникова',
          "bodyV2Markdown" = 'Партнер, потенциально может возвращаться к диалогу и к офисному формату. Есть смысл снова прогревать и проверять готовность по людям.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = 'fb359b86-e892-4928-9489-c25ad9b8c94f';

        UPDATE {SCHEMA}."task"
        SET
          title = 'Вернуть Марка Колесникова в диалог',
          "bodyV2Markdown" = 'Вернуть Марка в диалог и проверить, можно ли перевести его в активный партнерский режим.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = 'dc176a22-7546-4aa7-9f19-5dfec98ab19a';

        UPDATE {SCHEMA}."note"
        SET
          title = 'Старый контакт по Олегу Сидорову',
          "bodyV2Markdown" = 'Старый контакт, с ним можно поработать, но большого потока людей ждать не стоит. Лучше держать на связи и смотреть на редкие возможности.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '443442bb-197e-4ce8-8bda-98bbead91a9b';

        UPDATE {SCHEMA}."task"
        SET
          title = 'Проверить Олега Сидорова',
          "bodyV2Markdown" = 'Проверить контакт и понять, есть ли повод для мягкого follow-up.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '0a4d3502-e5dc-495f-8992-178ec43955d2';

        UPDATE {SCHEMA}."note"
        SET
          title = 'Контекст по Пичугину',
          "bodyV2Markdown" = 'Максимальный тариф подключен. Может идти по партнерке, но сейчас стагнация и осторожность. Нужен мягкий follow-up после обновления портфеля.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '4ed07555-6fca-4741-928c-7f4162509b5e';

        UPDATE {SCHEMA}."task"
        SET
          title = 'Актуализировать Пичугина',
          "bodyV2Markdown" = 'Актуализировать контакт и проверить, есть ли окно на партнерский разговор.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '711802d6-d0f6-46e7-918b-0a14fd8e7b2d';

        UPDATE {SCHEMA}."note"
        SET
          title = 'Текущий статус Ракова',
          "bodyV2Markdown" = 'Инвестор с нами с декабря 2025. Сейчас стагнация, в партнерку не готов, но контакт живой и его не надо потерять.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '4e80ff3b-1fb3-4b83-a03c-4f900f63deec';

        UPDATE {SCHEMA}."task"
        SET
          title = 'Проверить Ракова',
          "bodyV2Markdown" = 'Проверить, появился ли повод вернуться к партнерке или пополнению.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '8945ac35-4379-4386-8803-487939a07769';

        UPDATE {SCHEMA}."note"
        SET
          title = 'ARM x SoulMate и дальнейший контакт',
          "bodyV2Markdown" = 'Был на конференции и интересовался форматом участия. Можно возвращать к ARM, проверять интерес к инвестиции и партнерству.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '361395e6-9d58-4ec6-90de-4cedbe63a75a';

        UPDATE {SCHEMA}."task"
        SET
          title = 'Возобновить диалог с Романом Демидовым',
          "bodyV2Markdown" = 'Возобновить диалог и проверить интерес к следующему шагу по ARM.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '5b2ee97c-9647-4f3f-ace2-039bfe4a2adc';

        UPDATE {SCHEMA}."note"
        SET
          title = 'Осторожный контакт по Сане',
          "bodyV2Markdown" = 'Раньше был негатив, но хотел зайти. Контакт не бросать, но работать осторожно и только если есть нормальное окно.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = 'ce8fe9d6-be77-4a34-aa63-bd6e65fce067';

        UPDATE {SCHEMA}."task"
        SET
          title = 'Проверить Саню',
          "bodyV2Markdown" = 'Проверить, есть ли смысл мягко написать и посмотреть реакцию.',
          "updatedByName" = 'Alexandr RYZHKOV'
        WHERE id = '9c997ce6-df20-4af1-b0c7-cc73d7960100';

        COMMIT;
        """
    ).strip()
    run_sql(sql)


if __name__ == "__main__":
    main()
