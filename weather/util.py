from datetime import tzinfo, datetime
from constants import *
from termcolor import colored


def get_current_local_datetime() -> datetime:
    return datetime.now()


def get_current_utc_datetime() -> datetime:
    return datetime.utcnow()


def to_datetime(dt: int, timezone: tzinfo = None) -> datetime:
    return datetime.fromtimestamp(dt, timezone)


def format_datetime(date_time: datetime, fmt: str = "%A, %d %B %Y   %I:%M%p") -> str:
    return date_time.strftime(fmt)


def format_report_header(date_time: datetime, city: str, state: str,
                         fmt: str = "%A, %d %B %Y   %I:%M%p", bold: bool = True, with_newline: bool = True) -> str:
    return colored(
                format_datetime(date_time, fmt=fmt) +
                "\n" +
                f"{city}, {state}",
                attrs=(["bold"] if bold else None)) + ("\n" if with_newline else "")


def format_visibility(visibility: int) -> str:
    if visibility < 1000:
        return f"{visibility}" + UNITS_ALL["visibility"]["low"]

    return f"{(visibility / 1000):.1f}" + UNITS_ALL["visibility"]["high"]


def format_wind_deg(wind_deg: int, nsew_only: bool = False) -> str:
    if nsew_only:
        return WIND_DEG_QUADRANT[wind_deg // 45]

    return f"{wind_deg % 45}" + UNITS_ALL["wind_deg"][WIND_DEG_QUADRANT[wind_deg // 45]]
