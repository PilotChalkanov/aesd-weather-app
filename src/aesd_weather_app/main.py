from aesd_weather_app.observers.lcd import LCDisplay
from aesd_weather_app.sensors.humidity_sensor import HumiditySensor
from aesd_weather_app.sensors.outside_temp import OutsideTempSensor
from aesd_weather_app.sensors.temp_sensor import TempSensor
import logging

from aesd_weather_app.sensors.wind_sensor import WindSensor


def main():
    logger = logging.Logger("WeatherAppLogger")
    logger.setLevel("INFO")
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    temp_sensor = TempSensor("Temp", logger=logger)
    humidity_sensor = HumiditySensor("Humidity", logger=logger)
    wind_sensor = WindSensor("Wind", logger=logger)
    outside_temp_sensor = OutsideTempSensor("Outside Temp", logger=logger)
    lcd = LCDisplay(logger=logger)

    temp_sensor.register_observer(lcd)
    humidity_sensor.register_observer(lcd)
    wind_sensor.register_observer(lcd)
    outside_temp_sensor.register_observer(lcd)

    while True:
        for sensor in [temp_sensor, humidity_sensor, wind_sensor, outside_temp_sensor]:
            try:
                sensor.sensor_update()
                lcd.refresh_display()
            except Exception as e:
                logger.error(f"Error reading from {sensor.name} sensor: {e}")


if __name__ == "__main__":

    main()
