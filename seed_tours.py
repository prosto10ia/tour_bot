from db import init_db, reset_tours_catalog


def main() -> None:
    # Гарантируем наличие таблиц и заново загружаем каталог туров.
    init_db()
    inserted_count = reset_tours_catalog()
    print(f"Каталог туров обновлён. Загружено {inserted_count} записей.")


if __name__ == "__main__":
    main()
