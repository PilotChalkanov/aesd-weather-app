from abc import ABC, abstractmethod
from typing import Dict

from aesd_weather_app.sensors.base_sensor import BaseSensor


class Observer(ABC):
    def __init__(self):
        self.sensors: Dict[str, str] = {}

    @abstractmethod
    def update(self, sensor_name, data):
        raise NotImplementedError("Subclasses must implement the update method.")

    def attach_sensor(self, sensor: BaseSensor):
        self.sensors[sensor.name] = "0.0"
