import pytest

from aesd_weather_app.sensors.outside_temp import OutsideTempSensor
from aesd_weather_app.sensors.wind_sensor import WindSensor  # type: ignore


@pytest.fixture
def outside_temp_sensor(logger):
    return OutsideTempSensor(name="Outside Temperature Sensor", logger=logger)


@pytest.fixture
def outside_wind_sensor(logger):
    return WindSensor(name="Outside Wind Sensor", logger=logger)


def test_outside_temp_sensor_read(outside_temp_sensor):
    """Test the read method of the OutsideTempSensor."""
    temp = outside_temp_sensor.read()
    assert isinstance(temp, str), "The read method should return a string."
    assert temp.replace(
        ".", "", 1
    ).isdigit(), (
        "The read method should return a numeric string representing the temperature."
    )


def test_outside_wind_sensor_read(outside_wind_sensor):
    """Test the read method of the OutsideWindSensor."""
    wind = outside_wind_sensor.read()
    assert isinstance(wind, str), "The read method should return a string."
    assert (
        float(wind) >= 0
    ), "The read method should return a non-negative numeric string representing the wind speed."
