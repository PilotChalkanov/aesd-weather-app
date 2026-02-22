"""TempSensor class for the AESD Weather App."""

from .base_sensor import BaseSensor


class TempSensor(BaseSensor):

    AHT21_DEVICE_PATH = "/dev/aht21"

    def __init__(self, name, logger=None):
        super().__init__(name)
        self.logger = logger

    def read(self) -> str:
        """Reads temperature data from the AHT21 sensor and returns it as a string."""
        self.logger.debug(f"Reading temperature from {self.name} sensor.")
        with open(self.AHT21_DEVICE_PATH, "r") as sensor:
            line = sensor.read().strip()
            temp_c = None
            try:
                temp_c, _ = line.split()
                self.logger.debug(f"Read values - Temperature: {temp_c}°C")
            except ValueError as e:
                self.logger.error(f"Error parsing sensor data: {e}")
            if temp_c is not None:
                return temp_c
            else:
                self.logger.error("Temperature data is missing.")
                raise ValueError("Temperature data is missing.")

    def register_observer(self, observer):
        self.observers.append(observer)
