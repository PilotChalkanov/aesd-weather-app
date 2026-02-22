"""OutsideTempSensor class for the AESD Weather App."""

import requests  # type: ignore

from aesd_weather_app.observers.observer import Observer

from aesd_weather_app.sensors.base_sensor import BaseSensor


class OutsideTempSensor(BaseSensor):

    URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, name, logger):
        super().__init__(name)
        self.logger = logger

    def read(self) -> str:
        """
        Gets outside temperature data from Open-Meteo API and returns it as a string.
        """

        params = {
            "latitude": 43.2167,
            "longitude": 27.9167,
            "current": "temperature_2m",
        }
        responses = requests.get(self.URL, params=params, timeout=60)
        if responses.status_code == 200:
            data = responses.json()
            temp_c = data["current"]["temperature_2m"]
            self.logger.debug(f"Read values - Outside Temperature: {temp_c}°C")
            return str(temp_c)
        else:
            self.logger.error(
                f"Failed to fetch outside temperature data: {responses.status_code}"
            )
            raise ConnectionError(
                f"Failed to fetch outside temperature data: {responses.status_code}"
            )

    def register_observer(self, observer: Observer):
        self.observers.append(observer)
