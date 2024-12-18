from unittest.mock import patch, Mock
from weather_api import get_weather_data
import sqlite3

DB_TEST_NAME = 'weather_data.db'

@patch('requests.get')
def test_get_weather_data_failure(mock_get):
    conn, cursor = sqlite3.connect(DB_TEST_NAME, check_same_thread=False), None
    cursor = conn.cursor()

    # Mock API response
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    try:
        result = get_weather_data("InvalidCity", cursor, conn)
        assert result is None, "Некорректная обработка несуществующего города"

        print(True)
    except AssertionError:
        print(False)

if __name__ == "__main__":
    test_get_weather_data_failure()
