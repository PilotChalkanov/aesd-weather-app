from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, sensor_name, data):
        raise NotImplementedError("Subclasses must implement the update method.")
