import abc
from typing import Any
from weather_data import *


class Frequency:

    @abc.abstractmethod
    def __init__(self, point_data: dict[str, Any], point: int) -> None:
        pass


class FrequencyData:

    @abc.abstractmethod
    def __init__(self, data: list[dict[str, Any]], city: str, state: str) -> None:
        pass

    @abc.abstractmethod
    def at_point(self, point: int) -> Frequency:
        pass

    @abc.abstractmethod
    def print_report(self) -> None:
        pass

    @abc.abstractmethod
    def plot_data(self) -> None:
        pass


class Current:

    def __init__(self, data: dict[str, Any]) -> None:
        self.dt = int(data["dt"])
        self.sunrise = int(data["sunrise"])
        self.sunset = int(data["sunset"])
        self.temp = float(data["temp"])
        self.feels_like = float(data["feels_like"])
        self.pressure = float(data["pressure"])
        self.humidity = float(data["humidity"])
        self.dew_point = float(data["dew_point"])
        self.uvi = float(data["uvi"])
        self.clouds = float(data["clouds"])
        self.visibility = float(data["visibility"])
        self.wind_speed = float(data["wind_speed"])
        self.wind_deg = float(data["wind_speed"])
        self.weather = Weather(data["weather"][0], "current")
        self.rain = data["rain"]
        self.snow = data["snow"]

    def print_report(self) -> None:
        print(self)