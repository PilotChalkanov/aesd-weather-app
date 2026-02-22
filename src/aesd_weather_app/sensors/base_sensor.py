"""BaseSensor class for the AESD Weather App."""

from abc import ABC, abstractmethod
from typing import List
from aesd_weather_app.observers.observer import Observer


class BaseSensor(ABC):
    def __init__(self, name):
        self.name = name
        self.observers: List[Observer] = []

    @abstractmethod
    def read(self) -> str:
        """
        Abstract method to read data from the sensor. Subclasses must implement
        this method to return the sensor data as a string.
        """
        raise NotImplementedError("Subclasses must implement the read method.")

    def register_observer(self, observer: Observer) -> None:
        """Registers an observer to receive updates from this sensor."""
        self.observers.append(observer)

    def notify_observers(self) -> None:
        """Notifies all registered observers with the latest sensor data."""
        for o in self.observers:
            o.update(self.name, self.read())
