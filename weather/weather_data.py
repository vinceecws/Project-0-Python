from typing import Any
import datetime


def get_current_local_datetime(to_timestamp: bool = False) -> datetime:
    if to_timestamp:
        return datetime.datetime.now().timestamp()

    return datetime.datetime.now()


def get_current_utc_datetime(to_timestamp: bool = False) -> datetime:
    if to_timestamp:
        return datetime.datetime.utcnow().timestamp()

    return datetime.datetime.utcnow()


def format_datetime(dt: int, timezone: datetime.tzinfo = None, fmt: str = "%A, %d %B %Y") -> str:
    return datetime.datetime.fromtimestamp(dt, timezone).strftime(fmt)


class WeatherData:

    def __init__(self, data: dict[str, Any], city: str, state: str) -> None:
        lat = data["lat"]
        lon = data["lon"]
        timezone = datetime.timezone(datetime.timedelta(seconds=int(data["timezone_offset"])))

    def print_horizontal(self):
        pass

    def plot_time_data(self):
        pass


class Weather:

    def print_weather_icon(self):
        pass

    def print_report(self):
        pass
