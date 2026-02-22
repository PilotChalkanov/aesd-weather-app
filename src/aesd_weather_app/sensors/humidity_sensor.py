from aesd_weather_app.observers.observer import Observer

from .base_sensor import BaseSensor


class HumiditySensor(BaseSensor):

    AHT21_DEVICE_PATH = "/dev/aht21"

    def __init__(self, name, logger=None):
        super().__init__(name)
        self.logger = logger

    def read(self) -> str:
        self.logger.debug(f"Reading humidity from {self.name} sensor.")
        with open(self.AHT21_DEVICE_PATH, "r") as sensor:
            line = sensor.read().strip()
            humidity_pct = None
            try:
                _, humidity_pct = line.split()
                self.logger.debug(f"Read values - Humidity: {humidity_pct}%")
            except ValueError as e:
                self.logger.error(f"Error parsing sensor data: {e}")
            if humidity_pct is not None:
                return humidity_pct
            else:
                self.logger.error("Humidity data is missing.")
                raise ValueError("Humidity data is missing.")

    def register_observer(self, observer: Observer):
        self.observers.append(observer)
