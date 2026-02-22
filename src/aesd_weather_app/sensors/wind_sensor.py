"""OutsideWeatherSensor class for the AESD Weather App."""

import requests  # type: ignore

from aesd_weather_app.observers.observer import Observer

from aesd_weather_app.sensors.base_sensor import BaseSensor


class WindSensor(BaseSensor):

    URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, name, logger):
        super().__init__(name)
        self.logger = logger

    def read(self) -> str:
        """Gets outside wind data from Open-Meteo API and returns it as a string."""

        params = {
            "latitude": 43.2167,
            "longitude": 27.9167,
            "current": "wind_speed_10m",
        }
        responses = requests.get(self.URL, params=params, timeout=60)
        if responses.status_code == 200:
            data = responses.json()
            wind_speed = data["current"]["wind_speed_10m"]
            self.logger.debug(f"Read values - Outside Wind Speed: {wind_speed} m/s")
            return str(wind_speed)
        else:
            self.logger.error(
                f"Failed to fetch outside wind data: {responses.status_code}"
            )
            raise ConnectionError(
                f"Failed to fetch outside wind data: {responses.status_code}"
            )

    def register_observer(self, observer: Observer):
        self.observers.append(observer)
