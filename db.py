import sqlite3
from contextlib import closing
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "tour_agency.db"

MONTH_ORDER = {
    "Январь": 1,
    "Февраль": 2,
    "Март": 3,
    "Апрель": 4,
    "Май": 5,
    "Июнь": 6,
    "Июль": 7,
    "Август": 8,
    "Сентябрь": 9,
    "Октябрь": 10,
    "Ноябрь": 11,
    "Декабрь": 12,
}

TOURS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS tours (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tour_type TEXT NOT NULL,
    title TEXT NOT NULL,
    country TEXT NOT NULL,
    season TEXT NOT NULL,
    duration TEXT NOT NULL,
    hotel TEXT NOT NULL,
    price_text TEXT NOT NULL,
    description TEXT NOT NULL
)
"""

REQUESTS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    username TEXT,
    full_name TEXT NOT NULL,
    tour_id INTEGER NOT NULL,
    tour_type TEXT NOT NULL,
    title TEXT NOT NULL,
    country TEXT NOT NULL,
    season TEXT NOT NULL,
    duration TEXT NOT NULL,
    hotel TEXT NOT NULL,
    price_text TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'отправлена',
    created_at TEXT NOT NULL
)
"""

SEED_TOURS = [
    (
        "school",
        "Байкальские каникулы",
        "Россия",
        "Сентябрь 2026",
        "4 дня / 3 ночи",
        "Виктория 3*",
        "42 300 (без ж/д)",
        "Школьный тур на Байкал.",
    ),
    (
        "school",
        "Зимние каникулы на Байкале 2027",
        "Россия",
        "Январь 2027",
        "4 дня / 3 ночи",
        "Ангара 3* / Прибайкальская",
        "56 500 (без авиа/ж/д)",
        "Зимний школьный тур на Байкал.",
    ),
    (
        "school",
        "Белорусские каникулы",
        "Беларусь",
        "Июнь 2027",
        "6 дней / 6 ночей",
        "Минск, Брест 2* и 3*",
        "от 41 000 (группа 24+2)",
        "Школьная поездка в Беларусь.",
    ),
    (
        "school",
        "ВнеКлассный Санкт-Петербург",
        "Россия",
        "Октябрь 2026",
        "6 дней / 5 ночей",
        "Москва 4*",
        "от 51 400 (взрослые без авиа)",
        "Школьный тур в Санкт-Петербург.",
    ),
    (
        "school",
        "Москва — лучший город на Земле",
        "Россия",
        "Октябрь 2026",
        "5 дней / 4 ночи",
        "Селигерская 4*",
        "от 59 800 – 75 600 (с авиа)",
        "Школьный тур в Москву.",
    ),
    (
        "school",
        "Каникулы на Сахалине",
        "Россия",
        "Октябрь 2026",
        "4 дня / 3 ночи",
        "Юность / хостел",
        "от 38 600 (без авиа)",
        "Школьный тур на Сахалин.",
    ),
    (
        "school",
        "Знакомство с Сахалином (профориентация)",
        "Россия",
        "Октябрь 2026",
        "4 дня / 3 ночи",
        "Юность 2* / хостел",
        "от 37 500 (без авиа)",
        "Профориентационный школьный тур на Сахалин.",
    ),
    (
        "school",
        "Восточные узоры Казани",
        "Россия",
        "Ноябрь 2026",
        "6 дней / 5 ночей",
        "Карат / Амакс / Берисон 3*",
        "от 59 400 (без авиа)",
        "Школьный тур в Казань.",
    ),
    (
        "school",
        "Зарядись энергией Урала!",
        "Россия",
        "Ноябрь 2026",
        "5 дней / 4 ночи",
        "Екатеринбург-Центральный 3*",
        "58 700 (с авиа)",
        "Школьный тур на Урал.",
    ),
    (
        "school",
        "Путь к звёздам",
        "Россия",
        "Декабрь 2026",
        "2 дня",
        "Не указана",
        "от 34 600 (ДВ прописка)",
        "Вертикализация и пуск ракеты, программа на 2 дня.",
    ),
    (
        "group",
        "Солнечная Абхазия!",
        "Абхазия",
        "Сентябрь 2026",
        "9 дней / 8 ночей",
        "Черноморец / Бархатные сезоны",
        "60 900 (без авиа)",
        "Тур для сборной группы в Абхазию.",
    ),
    (
        "group",
        "Колоритный Харбин",
        "Китай",
        "Август 2026",
        "6 дней / 5 ночей",
        "Дзи Фэн 3*",
        "52 700",
        "Сборный тур в Харбин.",
    ),
    (
        "group",
        "Блистательный Санкт-Петербург",
        "Россия",
        "Октябрь 2026",
        "7 дней / 6 ночей",
        "Москва 4*",
        "от 73 770 (дети с авиа)",
        "Сборный тур в Санкт-Петербург.",
    ),
    (
        "group",
        "Бэйдайхэ, отдых у Жёлтого моря",
        "Китай",
        "Июль 2026",
        "14 дней / 13 ночей",
        "Транспортная",
        "71 500",
        "Отдых в Бэйдайхэ у Жёлтого моря.",
    ),
    (
        "group",
        "Бэйдайхэ, отдых у Жёлтого моря",
        "Китай",
        "Август 2026",
        "14 дней / 13 ночей",
        "Транспортная",
        "75 500",
        "Отдых в Бэйдайхэ у Жёлтого моря.",
    ),
    (
        "group",
        "Далянь",
        "Китай",
        "Июль 2026",
        "12 дней / 11 ночей",
        "Плаза 4* / Бинхай",
        "от 63 700 (взрослые)",
        "Тур для сборной группы в Далянь.",
    ),
    (
        "group",
        "Далянь",
        "Китай",
        "Август 2026",
        "12 дней / 11 ночей",
        "Плаза 4* / Бинхай",
        "от 63 700 (взрослые)",
        "Тур для сборной группы в Далянь.",
    ),
    (
        "group",
        "От мегаполиса к морю (Далянь + Вэйхай)",
        "Китай",
        "Июль 2026",
        "10 дней / 9 ночей",
        "Не указана",
        "от 88 960",
        "Маршрут Далянь + Вэйхай.",
    ),
    (
        "group",
        "От мегаполиса к морю (Далянь + Вэйхай)",
        "Китай",
        "Июль 2026",
        "10 дней / 9 ночей",
        "Не указана",
        "от 88 960",
        "Маршрут Далянь + Вэйхай.",
    ),
    (
        "group",
        "От мегаполиса к морю (Далянь + Вэйхай)",
        "Китай",
        "Сентябрь 2026",
        "10 дней / 9 ночей",
        "Не указана",
        "от 88 960",
        "Маршрут Далянь + Вэйхай.",
    ),
    (
        "group",
        "Байкальский лёд 2027",
        "Россия",
        "Февраль 2027",
        "5 дней / 4 ночи",
        "Прибайкальская / Байкалов Острог",
        "от 88 900 (без авиа)",
        "Зимний сборный тур на Байкал.",
    ),
    (
        "group",
        "Минские каникулы и Беловежская сказка",
        "Беларусь",
        "Ноябрь 2026",
        "8 дней / 7 ночей",
        "Беларусь 3* / Турист 3*",
        "от 75 800 (без авиа)",
        "Сборный тур в Беларусь.",
    ),
    (
        "group",
        "Москва новогодняя",
        "Россия",
        "Январь 2027",
        "5 дней / 4 ночи",
        "Ибис Октябрьское поле 3*",
        "от 47 950 (дети без авиа)",
        "Новогодний тур в Москву.",
    ),
    (
        "group",
        "Красная Москва против Шанели!",
        "Россия",
        "Март 2027",
        "5 дней / 4 ночи",
        "4* в центре",
        "от 53 600 (без авиа)",
        "Тематический тур к 8 марта.",
    ),
    (
        "group",
        "Москва — лучший город на Земле",
        "Россия",
        "Май 2027",
        "5 дней / 4 ночи",
        "Селигерская 4*",
        "от 64 000 – 72 000 (с авиа)",
        "Сборный тур в Москву.",
    ),
    (
        "group",
        "Февральские выходные на Сахалине 2027",
        "Россия",
        "Февраль 2027",
        "5 дней / 4 ночи",
        "Рубин 3*",
        "46 960",
        "Зимний сборный тур на Сахалин.",
    ),
    (
        "group",
        "Майские каникулы на Сахалине (сивучи)",
        "Россия",
        "Апрель 2027",
        "5 дней / 4 ночи",
        "Юность",
        "от 48 650 (без авиа)",
        "Сборный тур на Сахалин с программой по наблюдению за сивучами.",
    ),
    (
        "group",
        "От динозавров к космосу! (Благовещенск)",
        "Россия",
        "Сентябрь 2026",
        "5 дней / 4 ночи",
        "Дружба 3* / MERCURE 4*",
        "от 47 040 – 56 400",
        "Сборный тур в Благовещенск.",
    ),
    (
        "group",
        "Квест «От Земли до Марса»",
        "Россия",
        "Сентябрь 2026",
        "1 день",
        "—",
        "3 960 (20+2)",
        "Однодневный квест.",
    ),
    (
        "group",
        "Космодром «Восточный» (школьники / сборная)",
        "Россия",
        "Октябрь 2026",
        "1 день",
        "—",
        "от 9 200 (льготные)",
        "Однодневная поездка на космодром Восточный.",
    ),
    (
        "group",
        "Путь к звёздам (пуск ракеты, 1 день)",
        "Россия",
        "Июль 2026",
        "1 день",
        "—",
        "от 14 500 (льготные)",
        "Однодневная программа на пуск ракеты.",
    ),
    (
        "group",
        "Шамбала Пинежье (выезд из Благовещенска)",
        "Россия",
        "Май 2027",
        "1 день",
        "—",
        "8 000",
        "Однодневный выездной тур.",
    ),
    (
        "group",
        "Шамбала Пинежье (выезд из Благовещенска)",
        "Россия",
        "Июль 2026",
        "1 день",
        "—",
        "8 000",
        "Однодневный выездной тур.",
    ),
    (
        "group",
        "Шамбала Пинежье (выезд из Благовещенска)",
        "Россия",
        "Август 2026",
        "1 день",
        "—",
        "8 000",
        "Однодневный выездной тур.",
    ),
    (
        "group",
        "Шамбала Пинежье (выезд из Благовещенска)",
        "Россия",
        "Сентябрь 2026",
        "1 день",
        "—",
        "8 000",
        "Однодневный выездной тур.",
    ),
    (
        "group",
        "Шамбала Пинежье (выезд из Шимановска и др.)",
        "Россия",
        "Май 2027",
        "1 день",
        "—",
        "Не указана",
        "Однодневный выездной тур из Шимановска и других городов.",
    ),
    (
        "hot",
        "Горящий Байкал экспресс",
        "Россия",
        "Январь 2027",
        "4 дня / 3 ночи",
        "Виктория 3*",
        "39 900 (без ж/д)",
        "Горящий тур на Байкал на базе школьного маршрута.",
    ),
    (
        "hot",
        "Горящий ледяной Байкал",
        "Россия",
        "Февраль 2027",
        "5 дней / 4 ночи",
        "Прибайкальская / Байкалов Острог",
        "84 500 (без авиа)",
        "Горящий зимний тур на Байкал.",
    ),
    (
        "hot",
        "Горящий Санкт-Петербург",
        "Россия",
        "Октябрь 2026",
        "6 дней / 5 ночей",
        "Москва 4*",
        "от 47 900 (без авиа)",
        "Горящий тур в Санкт-Петербург с проживанием в отеле Москва 4*.",
    ),
    (
        "hot",
        "Горящая Москва на каникулы",
        "Россия",
        "Май 2027",
        "5 дней / 4 ночи",
        "Селигерская 4*",
        "от 58 000 (с авиа)",
        "Горящее предложение в Москву.",
    ),
    (
        "hot",
        "Горящий Сахалин",
        "Россия",
        "Май 2027",
        "5 дней / 4 ночи",
        "Юность",
        "от 44 900 (без авиа)",
        "Горящее предложение на Сахалин.",
    ),
    (
        "hot",
        "Горящий Харбин",
        "Китай",
        "Август 2026",
        "6 дней / 5 ночей",
        "Дзи Фэн 3*",
        "49 800",
        "Горящий тур в Харбин по сниженной цене.",
    ),
    (
        "hot",
        "Горящий Бэйдайхэ",
        "Китай",
        "Июль 2026",
        "14 дней / 13 ночей",
        "Транспортная",
        "68 500",
        "Горящее предложение на отдых у Жёлтого моря.",
    ),
    (
        "hot",
        "Горящий Далянь",
        "Китай",
        "Август 2026",
        "12 дней / 11 ночей",
        "Плаза 4* / Бинхай",
        "от 59 900",
        "Горящее предложение в Далянь.",
    ),
    (
        "hot",
        "Горящая Абхазия",
        "Абхазия",
        "Сентябрь 2026",
        "9 дней / 8 ночей",
        "Черноморец / Бархатные сезоны",
        "55 900 (без авиа)",
        "Горящий тур в Абхазию.",
    ),
    (
        "hot",
        "Горящий Минск и Беловежье",
        "Беларусь",
        "Ноябрь 2026",
        "8 дней / 7 ночей",
        "Беларусь 3* / Турист 3*",
        "от 69 500 (без авиа)",
        "Горящий тур в Беларусь.",
    ),
    (
        "individual",
        "Индивидуальный Байкал комфорт",
        "Россия",
        "Январь 2027",
        "4 дня / 3 ночи",
        "Виктория 3*",
        "от 63 500",
        "Индивидуальный тур на Байкал с гибкой программой.",
    ),
    (
        "individual",
        "Индивидуальный Байкал зима",
        "Россия",
        "Январь 2027",
        "4 дня / 3 ночи",
        "Ангара 3* / Прибайкальская",
        "от 78 000",
        "Индивидуальный зимний тур на Байкал.",
    ),
    (
        "individual",
        "Индивидуальный Санкт-Петербург",
        "Россия",
        "Октябрь 2026",
        "6 дней / 5 ночей",
        "Москва 4*",
        "от 74 800",
        "Индивидуальный тур в Санкт-Петербург.",
    ),
    (
        "individual",
        "Индивидуальная Москва классика",
        "Россия",
        "Май 2027",
        "5 дней / 4 ночи",
        "Селигерская 4*",
        "от 82 000",
        "Индивидуальный тур в Москву.",
    ),
    (
        "individual",
        "Индивидуальный Сахалин",
        "Россия",
        "Октябрь 2026",
        "4 дня / 3 ночи",
        "Юность / хостел",
        "от 59 500",
        "Индивидуальный тур на Сахалин.",
    ),
    (
        "individual",
        "Индивидуальный Казань восточная",
        "Россия",
        "Ноябрь 2026",
        "6 дней / 5 ночей",
        "Карат / Амакс / Берисон 3*",
        "от 81 400",
        "Индивидуальный тур в Казань.",
    ),
    (
        "individual",
        "Индивидуальный Урал",
        "Россия",
        "Ноябрь 2026",
        "5 дней / 4 ночи",
        "Екатеринбург-Центральный 3*",
        "от 76 300",
        "Индивидуальный тур на Урал.",
    ),
    (
        "individual",
        "Индивидуальный космодром Восточный",
        "Россия",
        "Декабрь 2026",
        "2 дня",
        "Не указана",
        "от 48 900",
        "Индивидуальная программа с посещением космодрома.",
    ),
    (
        "individual",
        "Индивидуальный Харбин",
        "Китай",
        "Август 2026",
        "6 дней / 5 ночей",
        "Дзи Фэн 3*",
        "от 68 500",
        "Индивидуальный тур в Харбин.",
    ),
    (
        "individual",
        "Индивидуальный Бэйдайхэ",
        "Китай",
        "Июль 2026",
        "14 дней / 13 ночей",
        "Транспортная",
        "от 96 000",
        "Индивидуальный отдых у Жёлтого моря.",
    ),
    (
        "individual",
        "Индивидуальный Далянь",
        "Китай",
        "Август 2026",
        "12 дней / 11 ночей",
        "Плаза 4* / Бинхай",
        "от 89 000",
        "Индивидуальный тур в Далянь.",
    ),
    (
        "individual",
        "Индивидуальный Далянь + Вэйхай",
        "Китай",
        "Сентябрь 2026",
        "10 дней / 9 ночей",
        "Не указана",
        "от 117 000",
        "Индивидуальный маршрут Далянь + Вэйхай.",
    ),
    (
        "individual",
        "Индивидуальная Абхазия",
        "Абхазия",
        "Сентябрь 2026",
        "9 дней / 8 ночей",
        "Черноморец / Бархатные сезоны",
        "от 84 500",
        "Индивидуальный тур в Абхазию.",
    ),
    (
        "individual",
        "Индивидуальная Беларусь",
        "Беларусь",
        "Июнь 2027",
        "6 дней / 6 ночей",
        "Минск, Брест 2* и 3*",
        "от 67 000",
        "Индивидуальный тур по Беларуси.",
    ),
    (
        "individual",
        "Индивидуальный Минск и Беловежье",
        "Беларусь",
        "Ноябрь 2026",
        "8 дней / 7 ночей",
        "Беларусь 3* / Турист 3*",
        "от 92 000",
        "Индивидуальный тур в Беларусь с Беловежской пущей.",
    ),
    (
        "group",
        "Шамбала Пинежье (выезд из Шимановска и др.)",
        "Россия",
        "Июль 2026",
        "1 день",
        "—",
        "Не указана",
        "Однодневный выездной тур из Шимановска и других городов.",
    ),
    (
        "group",
        "Шамбала Пинежье (выезд из Шимановска и др.)",
        "Россия",
        "Июль 2026",
        "1 день",
        "—",
        "Не указана",
        "Однодневный выездной тур из Шимановска и других городов.",
    ),
    (
        "group",
        "Шамбала Пинежье (выезд из Шимановска и др.)",
        "Россия",
        "Август 2026",
        "1 день",
        "—",
        "Не указана",
        "Однодневный выездной тур из Шимановска и других городов.",
    ),
    (
        "group",
        "Шамбала Пинежье (выезд из Шимановска и др.)",
        "Россия",
        "Сентябрь 2026",
        "1 день",
        "—",
        "Не указана",
        "Однодневный выездной тур из Шимановска и других городов.",
    ),
]


def init_db() -> None:
    # Создаём таблицы и приводим базу к актуальной схеме.
    with sqlite3.connect(DB_PATH) as connection:
        _ensure_requests_table(connection)
        _ensure_tours_table(connection)
        tours_count = connection.execute("SELECT COUNT(*) FROM tours").fetchone()[0]
        if tours_count == 0:
            _seed_tours(connection)
        connection.commit()


def _season_sort_key(season: str) -> tuple[int, int, str]:
    # Сортируем сезоны в формате "Месяц Год" по возрастанию.
    parts = season.split()
    if len(parts) >= 2 and parts[0] in MONTH_ORDER and parts[-1].isdigit():
        return (int(parts[-1]), MONTH_ORDER[parts[0]], season)
    return (9999, 99, season)


def _ensure_tours_table(connection: sqlite3.Connection) -> None:
    # Если schema устарела, пересоздаём таблицу туров.
    table_exists = connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'tours'"
    ).fetchone()
    if table_exists is None:
        connection.execute(TOURS_TABLE_SQL)
        return

    columns = [
        column_info[1]
        for column_info in connection.execute("PRAGMA table_info(tours)").fetchall()
    ]
    expected_columns = {
        "tour_type",
        "title",
        "country",
        "season",
        "duration",
        "hotel",
        "price_text",
        "description",
    }
    if not expected_columns.issubset(set(columns)):
        connection.execute("DROP TABLE tours")
        connection.execute(TOURS_TABLE_SQL)


def _ensure_requests_table(connection: sqlite3.Connection) -> None:
    # Если schema заявок устарела, пересоздаём таблицу заявок.
    table_exists = connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'requests'"
    ).fetchone()
    if table_exists is None:
        connection.execute(REQUESTS_TABLE_SQL)
        return

    columns = [
        column_info[1]
        for column_info in connection.execute("PRAGMA table_info(requests)").fetchall()
    ]
    expected_columns = {
        "user_id",
        "username",
        "full_name",
        "tour_id",
        "tour_type",
        "title",
        "country",
        "season",
        "duration",
        "hotel",
        "price_text",
        "status",
        "created_at",
    }
    if not expected_columns.issubset(set(columns)):
        connection.execute("DROP TABLE requests")
        connection.execute(REQUESTS_TABLE_SQL)


def _seed_tours(connection: sqlite3.Connection) -> None:
    # Наполняем таблицу туров стартовыми данными.
    connection.executemany(
        """
        INSERT INTO tours (
            tour_type,
            title,
            country,
            season,
            duration,
            hotel,
            price_text,
            description
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        SEED_TOURS,
    )


def reset_tours_catalog() -> int:
    # Полностью пересоздаём каталог туров из стартового набора.
    with sqlite3.connect(DB_PATH) as connection:
        _ensure_tours_table(connection)
        connection.execute("DELETE FROM tours")
        connection.execute("DELETE FROM sqlite_sequence WHERE name = 'tours'")
        _seed_tours(connection)
        connection.commit()
    return len(SEED_TOURS)


def get_available_countries(tour_type: str) -> list[str]:
    # Возвращаем страны, доступные для выбранного типа тура.
    with sqlite3.connect(DB_PATH) as connection:
        with closing(
            connection.execute(
                """
                SELECT DISTINCT country
                FROM tours
                WHERE tour_type = ?
                ORDER BY country
                """,
                (tour_type,),
            )
        ) as cursor:
            return [row[0] for row in cursor.fetchall()]


def get_available_months(tour_type: str, country: str) -> list[str]:
    # Возвращаем месяцы или сезоны, доступные для выбранного типа и страны.
    with sqlite3.connect(DB_PATH) as connection:
        with closing(
            connection.execute(
                """
                SELECT DISTINCT season
                FROM tours
                WHERE tour_type = ?
                  AND country = ?
                """,
                (tour_type, country),
            )
        ) as cursor:
            seasons = [row[0] for row in cursor.fetchall()]
            return sorted(seasons, key=_season_sort_key)


def get_hot_months() -> list[str]:
    # Оставляем логику под горящие туры, но сейчас данных для неё нет.
    with sqlite3.connect(DB_PATH) as connection:
        with closing(
            connection.execute(
                """
                SELECT DISTINCT season
                FROM tours
                WHERE tour_type = 'hot'
                """
            )
        ) as cursor:
            seasons = [row[0] for row in cursor.fetchall()]
            return sorted(seasons, key=_season_sort_key)


def get_tours_by_filters(tour_type: str, country: str, season: str) -> list[tuple]:
    # Возвращаем туры по типу, стране и сезону.
    with sqlite3.connect(DB_PATH) as connection:
        with closing(
            connection.execute(
                """
                SELECT
                    id,
                    title,
                    country,
                    season,
                    duration,
                    hotel,
                    price_text,
                    description
                FROM tours
                WHERE tour_type = ?
                  AND country = ?
                  AND season = ?
                ORDER BY id ASC
                """,
                (tour_type, country, season),
            )
        ) as cursor:
            return cursor.fetchall()


def get_hot_tours_by_month(season: str) -> list[tuple]:
    # Возвращаем горящие туры за выбранный сезон.
    with sqlite3.connect(DB_PATH) as connection:
        with closing(
            connection.execute(
                """
                SELECT
                    id,
                    title,
                    country,
                    season,
                    duration,
                    hotel,
                    price_text,
                    description
                FROM tours
                WHERE tour_type = 'hot'
                  AND season = ?
                ORDER BY id ASC
                """,
                (season,),
            )
        ) as cursor:
            return cursor.fetchall()


def get_tour_by_id(tour_id: int) -> tuple | None:
    # Возвращаем один тур по его идентификатору.
    with sqlite3.connect(DB_PATH) as connection:
        with closing(
            connection.execute(
                """
                SELECT
                    id,
                    tour_type,
                    title,
                    country,
                    season,
                    duration,
                    hotel,
                    price_text,
                    description
                FROM tours
                WHERE id = ?
                """,
                (tour_id,),
            )
        ) as cursor:
            return cursor.fetchone()


def save_request(
    user_id: int,
    username: str | None,
    full_name: str,
    tour_id: int,
    tour_type: str,
    title: str,
    country: str,
    season: str,
    duration: str,
    hotel: str,
    price_text: str,
    created_at: str,
) -> None:
    # Сохраняем отправленную заявку пользователя.
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO requests (
                user_id,
                username,
                full_name,
                tour_id,
                tour_type,
                title,
                country,
                season,
                duration,
                hotel,
                price_text,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                username,
                full_name,
                tour_id,
                tour_type,
                title,
                country,
                season,
                duration,
                hotel,
                price_text,
                created_at,
            ),
        )
        connection.commit()


def get_user_requests(user_id: int) -> list[tuple]:
    # Возвращаем заявки конкретного пользователя.
    with sqlite3.connect(DB_PATH) as connection:
        with closing(
            connection.execute(
                """
                SELECT
                    id,
                    title,
                    country,
                    season,
                    hotel,
                    price_text,
                    status,
                    created_at
                FROM requests
                WHERE user_id = ?
                ORDER BY id DESC
                """,
                (user_id,),
            )
        ) as cursor:
            return cursor.fetchall()


def get_all_requests() -> list[tuple]:
    # Возвращаем все поступившие заявки для менеджера.
    with sqlite3.connect(DB_PATH) as connection:
        with closing(
            connection.execute(
                """
                SELECT
                    id,
                    user_id,
                    username,
                    full_name,
                    title,
                    country,
                    season,
                    hotel,
                    price_text,
                    status,
                    created_at
                FROM requests
                ORDER BY id DESC
                """
            )
        ) as cursor:
            return cursor.fetchall()
