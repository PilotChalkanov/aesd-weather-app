from logging import Logger
from time import sleep
from typing import Dict, List, Optional

from aesd_weather_app.observers.observer import Observer
from aesd_weather_app.sensors.base_sensor import BaseSensor


class LCDisplay(Observer):

    LCD_DEV = "/dev/lcd1602"

    def __init__(self, logger: Logger):
        self.logger = logger
        self.sensors: Dict[str, str] = {}
    
    def attach_sensor(self, sensor: BaseSensor):
        self.sensors[sensor.name] = ""

    def update(self, sensor_name: str, data: str):
        """Update the LCD display with new sensor data."""        
        self.logger.info(f"LCD Display updated with {sensor_name}: {data}")
        self.sensors[sensor_name] = data

    def refresh_display(self):
        """Refresh the LCD display with current sensor data."""
        with open(self.LCD_DEV, 'w') as lcd:
            for sensor_name, data in self.sensors.items():
                try:
                    lcd.write(f"{sensor_name}: {data}\n")
                    self.logger.debug(f"Refreshed LCD with {sensor_name}: {data}")
                except Exception as e:
                    self.logger.error(f"Error updating LCD with {sensor_name}: {e}")
                sleep(4)