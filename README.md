[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

# AESD Weather App

Small Python weather application for a Raspberry Pi 4 embedded weather station that reads local sensor data and public weather API data, then pushes updates to an LCD character device.

## Features

- Reads **temperature** and **humidity** from `/dev/aht21` - which is implmented as client i2c device, refer to [i2c-aht21-driver src code](https://github.com/PilotChalkanov/i2c-aht21-driver)
- Reads **outside temperature** and **wind speed** from Open-Meteo API
- Uses an observer pattern to publish sensor updates to an LCD display
- Writes LCD output to `/dev/lcd1602`, again implemented as i2c client device, refer to [i2c-lcd-drivers src code](https://github.com/PilotChalkanov/i2c-lcd-drivers)
- Includes unit and integration tests with coverage support

## Runtime Flow

The main loop (every 5 seconds):

1. Poll all sensors
2. Notify `LCDisplay` on changed values
3. Refresh LCD with current sensor values

Main entrypoint: `src/aesd_weather_app/main.py`

## Project Structure

```text
src/aesd_weather_app/
├── main.py
├── observers/
│   ├── observer.py
│   └── lcd.py
└── sensors/
		├── base_sensor.py
		├── temp_sensor.py
		├── humidity_sensor.py
		├── outside_temp.py
		└── wind_sensor.py

tests/
├── unit_tests/
└── integration_tests/
```

## Requirements

- Python `>=3.11`
- Target device: Raspberry Pi 4
- Linux device files:
	- `/dev/aht21`
	- `/dev/lcd1602`
- Network access to:
	- `https://api.open-meteo.com/v1/forecast`

## Installation

### Option 1: Virtual environment + pip

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
pip install pytest pytest-cov black flake8 mypy
```

### Option 2: UV (if you use it)

```bash
uv sync
```

## Run

```bash
python -m aesd_weather_app.main
```

The app logs to:

- `/var/log/weather_app.log`

If writing there fails due to permissions, run with appropriate privileges or adjust logging destination in `main.py`.


## Notes for Embedded/Yocto

- Ensure the character devices are present inside target image (`/dev/aht21`, `/dev/lcd1602`)
- Ensure proper permissions for both device nodes and `/var/log/weather_app.log`
- Ensure outbound network connectivity for Open-Meteo calls

## Troubleshooting

- **`LCD device not found`**: verify `/dev/lcd1602` exists and driver is loaded.
- **`Permission denied` on LCD/log file**: update udev/file permissions or run with proper user/group.
- **API failures**: verify DNS/network and Open-Meteo availability.
- **No display updates**: sensor values may not have changed; updates are pushed when state changes.
