from unittest.mock import MagicMock, patch, mock_open
import pytest
from aesd_weather_app.sensors.humidity_sensor import HumiditySensor


def test_humidity_sensor_read_success(humidity_sensor):
    """Test the read method with mocked file open."""
    mock_data = "20.5 65.3\n"  # temp, humidity

    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = humidity_sensor.read()
        assert result == "65.3"


def test_humidity_sensor_read_file_not_found(humidity_sensor):
    """Test the read method when file doesn't exist."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            humidity_sensor.read()


def test_humidity_sensor_read_malformed_data(humidity_sensor):
    """Test the read method with malformed data."""
    mock_data = "invalid_data\n"

    with patch("builtins.open", mock_open(read_data=mock_data)):
        with pytest.raises(ValueError):
            humidity_sensor.read()


def test_temperature_sensor_read_success(temp_sensor):
    """Test the read method with mocked file open."""
    mock_data = "20.5 65.3\n"  # temp, humidity

    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = temp_sensor.read()
        assert result == "20.5"


def test_temperature_sensor_read_file_not_found(temp_sensor):
    """Test the read method when file doesn't exist."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            temp_sensor.read()


def test_temperature_sensor_read_malformed_data(temp_sensor):
    """Test the read method with malformed data."""
    mock_data = "invalid_data\n"

    with patch("builtins.open", mock_open(read_data=mock_data)):
        with pytest.raises(ValueError):
            temp_sensor.read()
