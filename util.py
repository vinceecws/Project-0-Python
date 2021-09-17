import re
import json

from typing import Any
from urllib import request, parse
from urllib.error import HTTPError
from config import BASE_URL, GEO_ENDPOINT, WEATHER_ENDPOINT, API_KEY, UNITS
from constants import EXCLUDE_OPTS


def get_geo(city: str, state: str, limit: int = 10) -> dict[str, str]:
    url = parse.urljoin(BASE_URL, GEO_ENDPOINT) + \
          f"?q={parse.quote_plus(city)},{parse.quote_plus(state)},US&limit={limit}&appid={API_KEY}"

    try:
        with request.urlopen(url) as req:
            res = json.loads(req.read())
    except HTTPError as err:
        raise err

    return next(({
        "lat": x["lat"],
        "lon": x["lon"],
        "city": x["name"],
        "state": x["state"]
    } for x in res
        if x["name"].lower() == city.lower() and
        x["state"].lower() == state.lower() and
        x["country"].lower() == "us"
    ), None)


def get_weather(lat: str, lon: str, exclude: str = None) -> dict[str, Any]:
    if exclude is not None:
        if exclude not in EXCLUDE_OPTS:
            raise ValueError("Invalid argument for exclude. Must be one of {}".format(EXCLUDE_OPTS))

        url = parse.urljoin(BASE_URL, WEATHER_ENDPOINT) + \
            f"?lat={lat}&lon={lon}&exclude={exclude}&appid={API_KEY}&units={UNITS}"
    else:
        url = parse.urljoin(BASE_URL, WEATHER_ENDPOINT) + \
            f"?lat={lat}&lon={lon}&appid={API_KEY}&units={UNITS}"

    try:
        with request.urlopen(url) as req:
            res = json.loads(req.read())
    except HTTPError as err:
        raise err

    return res


def extract_input(in_str: str) -> (str, str):
    # Like Queens,NY
    reg = "([A-Za-z -]+),([A-Za-z ]{2})$"
    res = re.search(reg, in_str.strip())

    if res is not None:
        return res.group(1), res.group(2)

    return "", ""


def print_banner() -> None:
    with open("graphic/home_banner.txt") as file:
        for line in file.readlines():
            print(line, end="")

    print("\n\n\n")


def clear() -> None:
    print("\u001b[2J")


def clear_and_print_banner() -> None:
    clear()
    print_banner()
