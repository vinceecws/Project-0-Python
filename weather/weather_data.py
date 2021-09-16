from typing import Any
from datetime import timezone as tz, timedelta
from .frequency import Current, Minutely, Hourly, Daily, Alerts


class WeatherData:

    def __init__(self, data: dict[str, Any], city: str, state: str) -> None:
        self._data = data
        self.lat = float(self._data["lat"])
        self.lon = float(self._data["lon"])
        self.city = city
        self.state = state
        self.timezone = tz(timedelta(seconds=int(data["timezone_offset"])))
        self._alerts = Alerts(self._data["alerts"], city, state, self.timezone) if "alerts" in self._data else None
        self._current = Current(self._data["current"], self.city, self.state, self.timezone)
        self._minutely = None
        self._hourly = None
        self._daily = None

    @property
    def alerts(self) -> Alerts:
        return self._alerts

    @property
    def current(self) -> Current:
        return self._current

    @property
    def minutely(self) -> Minutely:
        if self._minutely is None:
            self._minutely = Minutely(self._data["minutely"], self.city, self.state, self.timezone, self._current.dt)
        return self._minutely

    @property
    def hourly(self) -> Hourly:
        if self._hourly is None:
            self._hourly = Hourly(self._data["hourly"], self.city, self.state, self.timezone, self._current.dt)
        return self._hourly

    @property
    def daily(self) -> Daily:
        if self._daily is None:
            self._daily = Daily(self._data["daily"], self.city, self.state, self.timezone, self._current.dt)
        return self._daily
