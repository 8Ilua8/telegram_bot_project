import sqlite3
from db_handler import init_db, get_favorites, save_city

DB_TEST_NAME = 'weather_data.db'

def test_get_favorites():
    conn, cursor = sqlite3.connect(DB_TEST_NAME, check_same_thread=False), None
    init_db()
    cursor = conn.cursor()

    try:
        save_city("Berlin", cursor, conn)
        save_city("London", cursor, conn)
        favorites = get_favorites(cursor)

        assert "Berlin" in favorites, "Город Berlin отсутствует в избранном"
        assert "London" in favorites, "Город London отсутствует в избранном"

        print(True)
    except AssertionError:
        print(False)

if __name__ == "__main__":
    test_get_favorites()
