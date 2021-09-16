from datetime import tzinfo, datetime
from constants import *


def get_current_local_datetime() -> datetime:
    return datetime.now()


def get_current_utc_datetime() -> datetime:
    return datetime.utcnow()


def to_datetime(dt: int, timezone: tzinfo = None) -> datetime:
    return datetime.fromtimestamp(dt, timezone)


def format_datetime(date_time: datetime, fmt: str = "%A, %d %B %Y") -> str:
    return date_time.strftime(fmt)


def format_visibility(visibility: int) -> str:
    if visibility < 1000:
        return f"{visibility}" + UNITS_ALL["visibility"]["low"]

    return f"{(visibility / 1000):.1f}" + UNITS_ALL["visibility"]["high"]


def format_wind_deg(wind_deg: int, nsew_only: bool = False) -> str:
    if nsew_only:
        return WIND_DEG_QUADRANT[wind_deg % 45]

    return f"{wind_deg // 45}" + UNITS_ALL["wind_deg"][WIND_DEG_QUADRANT[wind_deg % 45]]