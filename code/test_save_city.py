import sqlite3
from db_handler import init_db, get_favorites, save_city

DB_TEST_NAME = 'weather_data.db'

def test_save_city():
    conn, cursor = sqlite3.connect(DB_TEST_NAME, check_same_thread=False), None
    init_db()
    cursor = conn.cursor()

    try:
        save_city("Paris", cursor, conn)
        cursor.execute("SELECT city FROM cities WHERE city = ?", ("Paris",))
        assert cursor.fetchone() is not None, "Город не добавлен в избранное"

        save_city("Paris", cursor, conn)  # Проверяем дублирование
        cursor.execute("SELECT COUNT(*) FROM cities WHERE city = ?", ("Paris",))
        assert cursor.fetchone()[0] == 1, "Дублирование записи в избранное"

        print(True)
    except AssertionError:
        print(False)

if __name__ == "__main__":
    test_save_city()
