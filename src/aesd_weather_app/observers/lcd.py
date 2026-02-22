from logging import Logger
from time import sleep
from typing import Dict
from aesd_weather_app.observers.observer import Observer


class LCDisplay(Observer):

    LCD_DEV = "/dev/lcd1602"

    def __init__(self, logger: Logger):
        self.logger = logger
        self.sensors: Dict[str, str] = {}

    def update(self, sensor_name: str, data: str):
        """Update the LCD display with new sensor data."""
        if sensor_name in self.sensors:
            self.logger.info(f"LCD Display updated with {sensor_name}: {data}")
            self.sensors[sensor_name] = data
        else:
            self.logger.warning(
                f"Received update for unregistered sensor: {sensor_name}"
            )

    def refresh_display(self):
        """Refresh the LCD display with current sensor data."""
        try:
            with open(self.LCD_DEV, "w") as lcd:
                for sensor_name, data in self.sensors.items():
                    lcd.write(f"{sensor_name}: {data}\n")
                    self.logger.debug(f"Refreshed LCD with {sensor_name}: {data}")
                sleep(3)
        except FileNotFoundError as e:
            self.logger.error(f"LCD device not found: {e}")
        except PermissionError as e:
            self.logger.error(f"Permission denied when accessing LCD device: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error while refreshing LCD display: {e}")
