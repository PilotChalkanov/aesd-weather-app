from aesd_weather_app.observers.lcd import LCDisplay
from aesd_weather_app.sensors.humidity_sensor import HumiditySensor
from aesd_weather_app.sensors.outside_temp import OutsideTempSensor
from aesd_weather_app.sensors.temp_sensor import TempSensor
import logging
from time import sleep

from aesd_weather_app.sensors.wind_sensor import WindSensor


def main():
    logging.basicConfig(
        filename="/var/log/weather_app.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
    )
    logger = logging.getLogger("WeatherAppLogger")

    temp_sensor = TempSensor("Temp", logger=logger)
    humidity_sensor = HumiditySensor("Humidity", logger=logger)
    wind_sensor = WindSensor("Wind", logger=logger)
    outside_temp_sensor = OutsideTempSensor("Out Temp", logger=logger)
    lcd = LCDisplay(logger=logger)

    temp_sensor.register_observer(lcd)
    humidity_sensor.register_observer(lcd)
    wind_sensor.register_observer(lcd)
    outside_temp_sensor.register_observer(lcd)
    sensors = [temp_sensor, humidity_sensor, wind_sensor, outside_temp_sensor]

    try:
        while True:
            for sensor in sensors:
                try:
                    sensor.sensor_update()
                except Exception:
                    logger.exception("Error reading from %s sensor", sensor.name)
            lcd.refresh_display()
            sleep(5)
    except KeyboardInterrupt:
        logger.info("Weather app stopped by user")


if __name__ == "__main__":

    main()
