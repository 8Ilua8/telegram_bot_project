import sqlite3
from db_handler import init_db

DB_TEST_NAME = 'weather_data.db'
# Функция для тестирования функции init_db
def test_init_db():
    # Создаем подключение к тестовой базе данных
    conn, _ = sqlite3.connect(DB_TEST_NAME, check_same_thread=False), None
    # Вызываем функцию инициализации базы данных, которая создает таблицы
    init_db()
    # Создаем объект курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    try:
        # Проверяем, что таблица 'weather' создана
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='weather'")
        assert cursor.fetchone() is not None, "Таблица 'weather' не создана"

        # Проверяем, что таблица 'cities' создана
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cities'")
        assert cursor.fetchone() is not None, "Таблица 'cities' не создана"

        # Если обе проверки пройдены, печатаем True
        print(True)
    except AssertionError as e:
        # Если одна из таблиц не создана, печатаем False
        print(False)


if __name__ == "__main__":
    test_init_db()
