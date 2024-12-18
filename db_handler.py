import sqlite3

DB_NAME = 'weather_data.db'

def init_db():
    """Инициализирует базу данных и возвращает соединение и курсор."""
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()

    # Создаем таблицу для погоды
    cursor.execute('''CREATE TABLE IF NOT EXISTS weather (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        city TEXT,
                        temperature REAL,
                        humidity INTEGER,
                        description TEXT,
                        date TEXT)''')

    # Создаем таблицу для избранных городов
    cursor.execute('''CREATE TABLE IF NOT EXISTS cities (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        city TEXT UNIQUE)''')

    conn.commit()
    return conn, cursor


def save_weather_data(city, temperature, humidity, description, date, cursor, conn):
    """Сохраняет данные о погоде в базу."""
    cursor.execute('''INSERT INTO weather (city, temperature, humidity, description, date) 
                      VALUES (?, ?, ?, ?, ?)''',
                   (city, temperature, humidity, description, date))
    conn.commit()


def save_city(city, cursor, conn):
    """Сохраняет город в избранное."""
    cursor.execute('INSERT OR IGNORE INTO cities (city) VALUES (?)', (city,))
    conn.commit()


def get_favorites(cursor):
    """Возвращает список избранных городов."""
    cursor.execute('SELECT city FROM cities')
    return [row[0] for row in cursor.fetchall()]

