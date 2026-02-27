import pytest

from aesd_weather_app.sensors.outside_temp import OutsideTempSensor  # type: ignore
from aesd_weather_app.sensors.wind_sensor import WindSensor  # type: ignore


@pytest.fixture
def outside_temp_sensor(logger):
    return OutsideTempSensor(name="Outside Temperature Sensor", logger=logger)


@pytest.fixture
def outside_wind_sensor(logger):
    return WindSensor(name="Outside Wind Sensor", logger=logger)
