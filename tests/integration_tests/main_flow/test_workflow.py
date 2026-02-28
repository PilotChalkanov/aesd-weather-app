from aesd_weather_app.observers.lcd import LCDisplay
from aesd_weather_app.main import main
from aesd_weather_app.sensors.outside_temp import OutsideTempSensor
from aesd_weather_app.sensors.humidity_sensor import HumiditySensor
from aesd_weather_app.sensors.temp_sensor import TempSensor
from aesd_weather_app.sensors.wind_sensor import WindSensor

from unittest.mock import call, mock_open, patch


def test_main_workflow(logger, outside_temp_sensor, outside_wind_sensor):
    """Test the main workflow of the application."""
    # Simulate sensor updates and check if the logger captures the expected output
    mock_temp_data = "20.5 65.3\n"  # temp, humidity
    temp_sensor = TempSensor(name="Test Temp", logger=logger)
    humidity_sensor = HumiditySensor(name="Test Humidity", logger=logger)

    lcd = LCDisplay(logger=logger)
    temp_sensor.register_observer(lcd)
    humidity_sensor.register_observer(lcd)
    outside_temp_sensor.register_observer(lcd)
    outside_wind_sensor.register_observer(lcd)

    with (
        patch("builtins.open", mock_open(read_data=mock_temp_data)) as mocked_open,
        patch.object(outside_temp_sensor, "read", return_value="18.2"),
        patch.object(outside_wind_sensor, "read", return_value="5.7"),
    ):
        temp_sensor.sensor_update()
        assert lcd.new_data, "Update message should be received by LCD observer"
        humidity_sensor.sensor_update()
        outside_temp_sensor.sensor_update()
        outside_wind_sensor.sensor_update()
        lcd.refresh_display()
        assert (
            not lcd.new_data
        ), "LCD should reset new_data flag after refreshing display"

        assert (
            temp_sensor._state == 20.5
        ), "Temperature sensor state should be updated to 20.5"
        assert (
            humidity_sensor._state == 65.3
        ), "Humidity sensor state should be updated to 65.3"
        assert (
            outside_temp_sensor._state == 18.2
        ), "Outside temperature sensor state should be updated to 18.2"
        assert (
            outside_wind_sensor._state == 5.7
        ), "Outside wind sensor state should be updated to 5.7"

        mocked_open.assert_any_call(LCDisplay.LCD_DEV, "w")
        lcd_handle = mocked_open()
        lcd_handle.write.assert_has_calls(
            [
                call("Test Temp: 20.5\n"),
                call("Test Humidity: 65.3\n"),
                call("Outside Temperature Sensor: 18.2\n"),
                call("Outside Wind Sensor: 5.7\n"),
            ],
            any_order=True,
        )


def test_main_runs_single_cycle_and_refreshes_display():
    """Test that main propagates concrete sensor read values to LCD output."""
    with (
        patch("builtins.open", mock_open()) as mocked_open,
        patch.object(TempSensor, "read", return_value="21.1") as temp_read,
        patch.object(HumiditySensor, "read", return_value="66.0") as humidity_read,
        # patch.object(WindSensor, "read", return_value="4.2") as wind_read,
        # patch.object(
        #     OutsideTempSensor, "read", return_value="17.9"
        # ) as outside_temp_read,
        patch("aesd_weather_app.main.sleep", side_effect=KeyboardInterrupt),
    ):
        main()

    temp_read.assert_called_once()
    humidity_read.assert_called_once()
    # wind_read.assert_called_once()
    # outside_temp_read.assert_called_once()

    mocked_open.assert_any_call(LCDisplay.LCD_DEV, "w")
    lcd_handle = mocked_open()
    lcd_handle.write.assert_has_calls(
        [
            call("Temp: 21.1\n"),
            call("Humidity: 66.0\n"),
            # call("Wind: 4.2\n"),
            # call("Out Temp: 17.9\n"),
        ],
        any_order=False,
    )
