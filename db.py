import sqlite3
from contextlib import closing
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "tour_agency.db"

SEED_TOURS = [
    ("Турция", "Июнь 2026", 3, 48000, "Аланья, Sun Melody, 3★, завтраки, 6 ночей", 0, None),
    ("Турция", "Июнь 2026", 4, 69000, "Анталья, Blue Wave Resort, 4★, всё включено, 7 ночей", 1, 82000),
    ("Турция", "Июнь 2026", 5, 118000, "Белек, Imperial берег, 5★, ultra all inclusive, 7 ночей", 0, None),
    ("Турция", "Июль 2026", 3, 56000, "Мармарис, Aegean Light, 3★, завтраки, 7 ночей", 0, None),
    ("Турция", "Июль 2026", 4, 79000, "Сиде, Palm Avenue, 4★, всё включено, 7 ночей", 0, None),
    ("Турция", "Июль 2026", 5, 134000, "Кемер, SunPeak Hotel, 5★, всё включено, 8 ночей", 1, 151000),
    ("Турция", "Август 2026", 3, 61000, "Бодрум, Lime Coast, 3★, завтраки, 6 ночей", 0, None),
    ("Турция", "Август 2026", 4, 86000, "Анталья, Azure Bay, 4★, всё включено, 7 ночей", 0, None),
    ("Турция", "Август 2026", 5, 142000, "Белек, Grand Sapphire, 5★, ultra all inclusive, 8 ночей", 0, None),
    ("Турция", "Сентябрь 2026", 3, 52000, "Аланья, Citrus Beach, 3★, завтраки, 7 ночей", 1, 64000),
    ("Турция", "Сентябрь 2026", 4, 74000, "Кемер, Garden Sea Club, 4★, всё включено, 7 ночей", 0, None),
    ("Турция", "Сентябрь 2026", 5, 126000, "Сиде, Royal Dunes, 5★, всё включено, 8 ночей", 0, None),
    ("Египет", "Июнь 2026", 3, 47000, "Хургада, Desert Palm, 3★, завтраки, 6 ночей", 0, None),
    ("Египет", "Июнь 2026", 4, 65000, "Хургада, Red Sea View, 4★, всё включено, 7 ночей", 0, None),
    ("Египет", "Июнь 2026", 5, 92000, "Шарм-эль-Шейх, Sunrise Reef, 5★, всё включено, 7 ночей", 1, 108000),
    ("Египет", "Июль 2026", 3, 51000, "Хургада, Coral Sand, 3★, завтраки, 7 ночей", 0, None),
    ("Египет", "Июль 2026", 4, 71000, "Макади Бей, Lotus Bay, 4★, всё включено, 7 ночей", 0, None),
    ("Египет", "Июль 2026", 5, 98000, "Шарм-эль-Шейх, Crystal Oasis, 5★, всё включено, 8 ночей", 0, None),
    ("Египет", "Август 2026", 3, 54000, "Хургада, Sea Echo, 3★, завтраки, 7 ночей", 0, None),
    ("Египет", "Август 2026", 4, 76000, "Сафага, Golden Coast, 4★, всё включено, 7 ночей", 0, None),
    ("Египет", "Август 2026", 5, 97000, "Шарм-эль-Шейх, Coral Garden, 5★, 7 ночей", 1, 112000),
    ("Египет", "Сентябрь 2026", 3, 49000, "Хургада, Marina Sun, 3★, завтраки, 6 ночей", 1, 59000),
    ("Египет", "Сентябрь 2026", 4, 69000, "Эль-Гуна, Velvet Bay, 4★, всё включено, 7 ночей", 0, None),
    ("Египет", "Сентябрь 2026", 5, 94000, "Шарм-эль-Шейх, Pharaoh Palace, 5★, всё включено, 7 ночей", 0, None),
    ("ОАЭ", "Июнь 2026", 3, 62000, "Шарджа, City Avenue, 3★, завтраки, 5 ночей", 0, None),
    ("ОАЭ", "Июнь 2026", 4, 91000, "Дубай, Marina Edge, 4★, завтраки, 6 ночей", 0, None),
    ("ОАЭ", "Июнь 2026", 5, 148000, "Абу-Даби, Pearl Crown, 5★, завтраки, 6 ночей", 0, None),
    ("ОАЭ", "Июль 2026", 3, 66000, "Шарджа, Gulf Walk, 3★, завтраки, 5 ночей", 0, None),
    ("ОАЭ", "Июль 2026", 4, 98000, "Дубай, Palm Line, 4★, завтраки, 6 ночей", 0, None),
    ("ОАЭ", "Июль 2026", 5, 152000, "Рас-эль-Хайма, Mirage Palace, 5★, полупансион, 7 ночей", 0, None),
    ("ОАЭ", "Август 2026", 3, 64000, "Аджман, Sand City, 3★, завтраки, 5 ночей", 0, None),
    ("ОАЭ", "Август 2026", 4, 103000, "Дубай, Bay Central, 4★, завтраки, 6 ночей", 0, None),
    ("ОАЭ", "Август 2026", 5, 159000, "Абу-Даби, Corniche Grand, 5★, завтраки, 6 ночей", 0, None),
    ("ОАЭ", "Сентябрь 2026", 3, 59000, "Шарджа, Lagoon Point, 3★, завтраки, 5 ночей", 0, None),
    ("ОАЭ", "Сентябрь 2026", 4, 109000, "Дубай, Marina Palm, 4★, завтраки, 6 ночей", 1, 124000),
    ("ОАЭ", "Сентябрь 2026", 5, 146000, "Фуджейра, Ocean Crest, 5★, полупансион, 7 ночей", 0, None),
    ("Таиланд", "Июнь 2026", 3, 70000, "Паттайя, Tropic Smile, 3★, завтраки, 8 ночей", 0, None),
    ("Таиланд", "Июнь 2026", 4, 96000, "Пхукет, Andaman Pearl, 4★, завтраки, 8 ночей", 0, None),
    ("Таиланд", "Июнь 2026", 5, 138000, "Самуи, Emerald Cape, 5★, завтраки, 9 ночей", 0, None),
    ("Таиланд", "Июль 2026", 3, 76000, "Пхукет, Island Vibe, 3★, завтраки, 8 ночей", 0, None),
    ("Таиланд", "Июль 2026", 4, 102000, "Паттайя, Siam Breeze, 4★, завтраки, 8 ночей", 0, None),
    ("Таиланд", "Июль 2026", 5, 149000, "Паттайя, Royal Lotus, 5★, завтраки, 8 ночей", 1, 169000),
    ("Таиланд", "Август 2026", 3, 82000, "Пхукет, Sea Mist Inn, 3★, завтраки, 9 ночей", 0, None),
    ("Таиланд", "Август 2026", 4, 108000, "Краби, Sunset Cliff, 4★, завтраки, 8 ночей", 0, None),
    ("Таиланд", "Август 2026", 5, 154000, "Пхи-Пхи, Lagoon Select, 5★, завтраки, 9 ночей", 0, None),
    ("Таиланд", "Сентябрь 2026", 3, 88000, "Пхукет, Sea Breeze Inn, 3★, 9 ночей", 1, 99000),
    ("Таиланд", "Сентябрь 2026", 4, 112000, "Паттайя, Azure Tropics, 4★, завтраки, 8 ночей", 0, None),
    ("Таиланд", "Сентябрь 2026", 5, 158000, "Самуи, Lotus Reserve, 5★, завтраки, 9 ночей", 0, None),
]


def init_db() -> None:
    # Создаём таблицы и наполняем каталог туров стартовыми данными.
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT,
                "тип_заявки" TEXT NOT NULL,
                "текст" TEXT NOT NULL,
                "дата" TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tours (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                country TEXT NOT NULL,
                dates TEXT NOT NULL,
                stars INTEGER NOT NULL,
                price INTEGER NOT NULL,
                title TEXT NOT NULL,
                is_hot INTEGER NOT NULL DEFAULT 0,
                old_price INTEGER
            )
            """
        )
        tours_count = connection.execute("SELECT COUNT(*) FROM tours").fetchone()[0]
        if tours_count == 0:
            _seed_tours(connection)
        connection.commit()


def _seed_tours(connection: sqlite3.Connection) -> None:
    # Наполняем таблицу tours стартовыми турами.
    connection.executemany(
        """
        INSERT INTO tours (
            country, dates, stars, price, title, is_hot, old_price
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        SEED_TOURS,
    )


def reset_tours_catalog() -> int:
    # Полностью пересоздаём каталог туров из стартового набора.
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tours (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                country TEXT NOT NULL,
                dates TEXT NOT NULL,
                stars INTEGER NOT NULL,
                price INTEGER NOT NULL,
                title TEXT NOT NULL,
                is_hot INTEGER NOT NULL DEFAULT 0,
                old_price INTEGER
            )
            """
        )
        connection.execute("DELETE FROM tours")
        _seed_tours(connection)
        connection.commit()
    return len(SEED_TOURS)


def save_request(
    user_id: int,
    username: str | None,
    request_type: str,
    text: str,
    created_at: str,
) -> None:
    # Сохраняем новую заявку пользователя.
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO requests (user_id, username, "тип_заявки", "текст", "дата")
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, username, request_type, text, created_at),
        )
        connection.commit()


def get_user_requests(user_id: int) -> list[tuple]:
    # Возвращаем все заявки пользователя, начиная с последних.
    with sqlite3.connect(DB_PATH) as connection:
        with closing(
            connection.execute(
                """
                SELECT id, username, "тип_заявки", "текст", "дата"
                FROM requests
                WHERE user_id = ?
                ORDER BY id DESC
                """,
                (user_id,),
            )
        ) as cursor:
            return cursor.fetchall()


def get_last_user_request(user_id: int) -> tuple | None:
    # Получаем последнюю заявку пользователя для отправки менеджеру.
    with sqlite3.connect(DB_PATH) as connection:
        with closing(
            connection.execute(
                """
                SELECT id, username, "тип_заявки", "текст", "дата"
                FROM requests
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (user_id,),
            )
        ) as cursor:
            return cursor.fetchone()


def get_matching_tours(
    country: str,
    dates: str,
    stars: int,
    budget: int,
    limit: int = 3,
) -> list[tuple]:
    # Ищем туры по выбранным параметрам в пределах бюджета.
    with sqlite3.connect(DB_PATH) as connection:
        with closing(
            connection.execute(
                """
                SELECT title, price
                FROM tours
                WHERE country = ?
                  AND dates = ?
                  AND stars = ?
                  AND price <= ?
                ORDER BY price ASC, id ASC
                LIMIT ?
                """,
                (country, dates, stars, budget, limit),
            )
        ) as cursor:
            return cursor.fetchall()


def get_fallback_tours(
    country: str,
    dates: str,
    stars: int,
    limit: int = 3,
) -> list[tuple]:
    # Если бюджет слишком низкий, показываем ближайшие варианты по тем же фильтрам.
    with sqlite3.connect(DB_PATH) as connection:
        with closing(
            connection.execute(
                """
                SELECT title, price
                FROM tours
                WHERE country = ?
                  AND dates = ?
                  AND stars = ?
                ORDER BY price ASC, id ASC
                LIMIT ?
                """,
                (country, dates, stars, limit),
            )
        ) as cursor:
            return cursor.fetchall()


def get_hot_tours(limit: int = 3) -> list[tuple]:
    # Возвращаем несколько горящих туров из базы.
    with sqlite3.connect(DB_PATH) as connection:
        with closing(
            connection.execute(
                """
                SELECT title, price, old_price
                FROM tours
                WHERE is_hot = 1
                ORDER BY price ASC, id ASC
                LIMIT ?
                """,
                (limit,),
            )
        ) as cursor:
            return cursor.fetchall()
