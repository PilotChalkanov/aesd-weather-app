import pytest

from aesd_weather_app.sensors.humidity_sensor import HumiditySensor



@pytest.fixture
def humidity_sensor(logger):
    """Fixture for providing a HumiditySensor instance for tests."""
    return HumiditySensor(name="Test Humidity", logger=logger)

@pytest.fixture
def temp_sensor(logger):
    """Fixture for providing a TempSensor instance for tests."""
    from aesd_weather_app.sensors.temp_sensor import TempSensor
    return TempSensor(name="Test Temp", logger=logger)