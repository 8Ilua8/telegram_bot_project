import requests
from datetime import datetime
from db_handler import save_weather_data

API_KEY = '105906636a28682635d611660b502f2b'

def get_weather_data(city, cursor, conn):
    """Получает данные о погоде для указанного города через API."""
    URL = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru'
    response = requests.get(URL)

    if response.status_code != 200:
        return None

    data = response.json()

    city_name = data['name']
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    description = data['weather'][0]['description']

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Сохраняем данные о погоде в базе
    save_weather_data(city_name, temperature, humidity, description, current_time, cursor, conn)

    return f'\U0001F3D9 Город: {city_name}\n\u2600 Температура: {temperature}°C\n\u2614 Влажность: {humidity}%\n\u2705 Описание: {description}'

