import abc
import plotext as plt
import numpy as np

from .util import *
from constants import *
from config import *
from typing import Any
from datetime import tzinfo
from tabulate import tabulate
from termcolor import colored


class Frequency:

    @abc.abstractmethod
    def __init__(self, point_data: dict[str, Any], point: int, timezone: tzinfo) -> None:
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


class Weather:

    def __init__(self, data: dict[str, Any], frequency: str) -> None:
        self.frequency = frequency
        self.id = int(data["id"])
        self.main = data["main"]
        self.description = data["description"]
        self.icon = data["icon"]

    def print_weather_icon(self) -> None:
        pass

    def print_report(self) -> None:
        pass


class Current:

    def __init__(self, data: dict[str, Any], city: str, state: str, timezone: tzinfo) -> None:
        self.city = city
        self.state = state
        self.timezone = timezone
        self.dt = to_datetime(int(data["dt"]), self.timezone)
        self.sunrise = int(data["sunrise"])
        self.sunset = int(data["sunset"])
        self.temp = float(data["temp"])
        self.feels_like = float(data["feels_like"])
        self.pressure = int(data["pressure"])
        self.humidity = int(data["humidity"])
        self.dew_point = float(data["dew_point"])
        self.uvi = float(data["uvi"])
        self.clouds = int(data["clouds"])
        self.visibility = int(data["visibility"])
        self.wind_speed = int(data["wind_speed"])
        self.wind_deg = int(data["wind_speed"])
        self.weather = Weather(data["weather"][0], "current")
        self.rain = float(data["rain"]["1h"]) if "rain" in data else None
        self.snow = float(data["snow"]["1h"]) if "snow" in data else None

    def print_report(self) -> None:
        print(format_datetime(self.dt))
        print(f"{self.city}, {self.state}")

        print(f"Current Weather: {self.weather.description.capitalize()}.")
        self.weather.print_report()

        data = [
            ["Temperature", f"{self.temp:.2f}" + UNITS_LIB[UNITS]["temp"]],
            ["Feels Like", f"{self.feels_like:.2f}" + UNITS_LIB[UNITS]["feels_like"]],
            ["Visibility", format_visibility(self.visibility)],
            ["Humidity", f"{self.humidity}" + UNITS_ALL["humidity"]],
            ["Pressure", f"{self.pressure}" + UNITS_ALL["pressure"]],
            ["Wind", f"{self.wind_speed}" + UNITS_LIB[UNITS]["wind_speed"] + " " +
             format_wind_deg(self.wind_deg, nsew_only=True)]
        ]

        print(tabulate(data))


class Minutely(FrequencyData):

    class Minute(Frequency):
        frequency = "minutely"

        def __init__(self, data: dict[str, Any], point: int, timezone: tzinfo):
            self.point = point
            self.dt = to_datetime(int(data["dt"]), timezone)
            self.precipitation = float(data["precipitation"])

    def __init__(self, data: list[dict[str, Any]], city: str, state: str, timezone: tzinfo) -> None:
        self.city = city
        self.state = state
        self.timezone = timezone
        self._data = [Minutely.Minute(x, i, self.timezone) for i, x in enumerate(data)]

    def at_point(self, point: int) -> Minute:
        return self._data[point]

    def print_report(self, num_points: int = 60) -> None:
        print(format_datetime(self._data[0].dt))
        print(f"{self.city}, {self.state}")

        print(
            f"Mean precipitation for the next {num_points}-minute: ",
            f"{np.mean([x.precipitation for x in self._data[:num_points]]):.2f}",
            UNITS_ALL["precipitation"]
        )

    def plot_data(self, num_points: int = 60) -> None:
        precipitation = [y.precipitation for y in self._data[:num_points]]
        x_labels = [format_datetime(x.dt, fmt="%I:%M%p") for x in self._data[:num_points]]
        x_ticks = list(range(len(x_labels)))
        plt.title(f"{num_points}-MINUTE PRECIPITATION FORECAST")
        plt.scatter(precipitation, label="Precipitation " + UNITS_ALL["precipitation"], marker=PLOT_MARKER_1)
        plt.plotsize(PLOT_SIZE_X, PLOT_SIZE_Y)
        plt.ticks(None, len(x_labels))
        plt.xticks(x_ticks, x_labels)
        if PLOT_CANVAS_COLOR is not None:
            plt.canvas_color(PLOT_CANVAS_COLOR)
        if PLOT_AXES_COLOR is not None:
            plt.axes_color(PLOT_AXES_COLOR)
        if PLOT_TICKS_COLOR is not None:
            plt.ticks_color(PLOT_TICKS_COLOR)
        plt.show()
        plt.clear_figure()


class Hourly(FrequencyData):

    class Hour(Frequency):
        frequency = "hourly"

        def __init__(self, data: dict[str, Any], point: int, timezone: tzinfo) -> None:
            self.point = point
            self.dt = to_datetime(int(data["dt"]), timezone)
            self.temp = float(data["temp"])
            self.feels_like = float(data["feels_like"])
            self.pressure = int(data["pressure"])
            self.humidity = int(data["humidity"])
            self.dew_point = float(data["dew_point"])
            self.uvi = float(data["uvi"])
            self.clouds = int(data["clouds"])
            self.visibility = int(data["visibility"])
            self.wind_speed = int(data["wind_speed"])
            self.wind_deg = int(data["wind_speed"])
            self.weather = Weather(data["weather"][0], self.frequency)
            self.pop = float(data["pop"])
            self.rain = float(data["rain"]["1h"]) if "rain" in data else None
            self.snow = float(data["snow"]["1h"]) if "snow" in data else None

    def __init__(self, data: list[dict[str, Any]], city: str, state: str, timezone: tzinfo) -> None:
        self.city = city
        self.state = state
        self.timezone = timezone
        self._data = [Hourly.Hour(x, i, self.timezone) for i, x in enumerate(data)]

    def at_point(self, point: int) -> Hour:
        return self._data[point]

    def print_report(self, num_points: int = 24) -> None:
        print(format_datetime(self._data[0].dt))
        print(f"{self.city}, {self.state}")

        data = [[
            format_datetime(x.dt, fmt="%I%p"),
            f"{round(x.temp):d}" + UNITS_LIB[UNITS]["temp"],
            f"{round(x.pop * 100):d}" + UNITS_ALL["pop"],
            f"{x.wind_speed}{UNITS_LIB[UNITS]['wind_speed']} {format_wind_deg(x.wind_deg, nsew_only=True)}",
            x.weather.description.capitalize()
        ] for x in self._data[:num_points]]

        headers = ["Time", "Temperature", "% of Rain", "Wind", "Weather"]

        print(tabulate(data, headers))

    def plot_data(self, num_points: int = 24) -> None:
        temp = [y.temp for y in self._data[:num_points]]
        feels_like = [y.feels_like for y in self._data[:num_points]]
        x_labels = [format_datetime(x.dt, fmt="%I%p") for x in self._data[:num_points]]
        x_ticks = list(range(len(x_labels)))
        plt.title(f"{num_points}-HOUR TEMPERATURE FORECAST")
        plt.scatter(temp, label="Temperature " + UNITS_LIB[UNITS]["temp"], marker=PLOT_MARKER_1)
        plt.scatter(feels_like, label="Feels Like " + UNITS_LIB[UNITS]["feels_like"], marker=PLOT_MARKER_2)
        plt.plotsize(PLOT_SIZE_X, PLOT_SIZE_Y)
        plt.ticks(None, len(x_labels))
        plt.xticks(x_ticks, x_labels)
        if PLOT_CANVAS_COLOR is not None:
            plt.canvas_color(PLOT_CANVAS_COLOR)
        if PLOT_AXES_COLOR is not None:
            plt.axes_color(PLOT_AXES_COLOR)
        if PLOT_TICKS_COLOR is not None:
            plt.ticks_color(PLOT_TICKS_COLOR)
        plt.show()
        plt.clear_figure()


class Daily(FrequencyData):

    class Day(Frequency):
        frequency = "daily"

        def __init__(self, data: dict[str, Any], point: int, timezone: tzinfo) -> None:
            self.point = point
            self.dt = to_datetime(int(data["dt"]), timezone)
            self.temp = {key: float(val) for key, val in data["temp"].items()}
            self.feels_like = {key: float(val) for key, val in data["feels_like"].items()}
            self.pressure = int(data["pressure"])
            self.humidity = int(data["humidity"])
            self.dew_point = float(data["dew_point"])
            self.uvi = float(data["uvi"])
            self.clouds = int(data["clouds"])
            self.wind_speed = int(data["wind_speed"])
            self.wind_deg = int(data["wind_speed"])
            self.weather = Weather(data["weather"][0], self.frequency)
            self.pop = float(data["pop"])
            self.rain = float(data["rain"]) if "rain" in data else None
            self.snow = float(data["snow"]) if "snow" in data else None

    def __init__(self, data: list[dict[str, Any]], city: str, state: str, timezone: tzinfo) -> None:
        self.city = city
        self.state = state
        self.timezone = timezone
        self._data = [Daily.Day(x, i, self.timezone) for i, x in enumerate(data)]

    def at_point(self, point: int) -> Day:
        return self._data[point]

    def print_report(self, num_points: int = 24) -> None:
        print(format_datetime(self._data[0].dt))
        print(f"{self.city}, {self.state}")

        data = [
            ["High"] + [f"{round(x.temp['max']):d}" + UNITS_LIB[UNITS]["temp"] for x in self._data[:num_points]],
            ["Low"] + [f"{round(x.temp['min']):d}" + UNITS_LIB[UNITS]["temp"] for x in self._data[:num_points]],
            ["% of Rain"] + [f"{round(x.pop * 100):d}" + UNITS_ALL["pop"] for x in self._data[:num_points]],
            ["Wind"] + [f"{x.wind_speed}{UNITS_LIB[UNITS]['wind_speed']} {format_wind_deg(x.wind_deg, nsew_only=True)}"
                        for x in self._data[:num_points]],
            ["Weather"] + [x.weather.main for x in self._data[:num_points]],
            [""] + [x.weather.description.capitalize() for x in self._data[:num_points]]
        ]

        headers = [""] + ["Today"] + [format_datetime(x.dt, fmt="%a, %b %d") for x in self._data[1:num_points]]

        print(tabulate(data, headers))

    def plot_data(self, num_points: int = 7) -> None:
        temp = [round(y.temp["max"] + y.temp["min"]) / 2 for y in self._data[:num_points]]
        feels_like = [round(max(y.feels_like.values()) + min(y.feels_like.values())) / 2 for y in self._data[:num_points]]
        x_labels = [format_datetime(x.dt, fmt="%a") for x in self._data[:num_points]]
        x_ticks = list(range(len(x_labels)))
        plt.title(f"{num_points}-DAY TEMPERATURE FORECAST")
        plt.scatter(temp, label="Avg. Temperature " + UNITS_LIB[UNITS]["temp"], marker=PLOT_MARKER_1)
        plt.scatter(feels_like, label="Feels Like " + UNITS_LIB[UNITS]["feels_like"], marker=PLOT_MARKER_2)
        plt.plotsize(PLOT_SIZE_X, PLOT_SIZE_Y)
        plt.ticks(None, len(x_labels))
        plt.xticks(x_ticks, x_labels)
        if PLOT_CANVAS_COLOR is not None:
            plt.canvas_color(PLOT_CANVAS_COLOR)
        if PLOT_AXES_COLOR is not None:
            plt.axes_color(PLOT_AXES_COLOR)
        if PLOT_TICKS_COLOR is not None:
            plt.ticks_color(PLOT_TICKS_COLOR)
        plt.show()
        plt.clear_figure()


class Alerts:

    class Alert:

        def __init__(self, data: dict[str, Any], ind: int, timezone: tzinfo) -> None:
            self.ind = ind
            self.sender_name = data["sender_name"]
            self.event = data["event"]
            self.start = to_datetime(int(data["start"]), timezone)
            self.end = to_datetime(int(data["end"]), timezone)
            self.description = data["description"]

    def __init__(self, data: list[dict[str, Any]], city: str, state: str, timezone: tzinfo) -> None:
        self.city = city
        self.state = state
        self._data = [Alerts.Alert(x, i, timezone) for i, x in enumerate(data)]

    def at_ind(self, ind: int) -> Alert:
        return self._data[ind]
