from setuptools import find_packages, setup

setup(
    name="aesd-weather-app",
    version="0.1.0",
    description="Simple app to read data from a I2C sensor and weather APIs and display to a LCD screen",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=[
        "requests>=2.0.0",
    ],
)