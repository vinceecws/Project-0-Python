import json
import re
import urllib.request as request
import urllib.parse as parse
import config

from urllib.error import HTTPError

API_KEY = config.API_KEY
UNITS = "imperial"
BASE_URL = "http://api.openweathermap.org/"
GEO_ENDPOINT = "/geo/1.0/direct"
WEATHER_ENDPOINT = "/data/2.5/onecall"
EXCLUDE_OPTS = {"current", "minutely", "hourly", "daily", "alerts"}


def get_geo(city: str, state: str, limit: int = 10) -> dict[str, str]:
    url = parse.urljoin(BASE_URL, GEO_ENDPOINT) + \
          "?q={},{},US&limit={}&appid={}".format(city, state, limit, API_KEY)
    try:
        res = json.loads(request.urlopen(url).read())
    except HTTPError as err:
        raise HTTPError("Error code: {}".format(err.code))

    return res


def get_weather(lat: str, lon: str, exclude: str = None) -> dict[str, object]:
    if exclude is not None:
        if exclude not in EXCLUDE_OPTS:
            raise ValueError("Invalid argument for exclude. Must be one of {}".format(EXCLUDE_OPTS))
        else:
            url = parse.urljoin(BASE_URL, WEATHER_ENDPOINT) + \
                  "?lat={}&lon={}&exclude={}&appid={}&units={}".format(lat, lon, exclude, API_KEY, UNITS)
    else:
        url = parse.urljoin(BASE_URL, WEATHER_ENDPOINT) + \
              "?lat={}&lon={}&appid={}&units={}".format(lat, lon, API_KEY, UNITS)

    try:
        res = json.loads(request.urlopen(url).read())
    except HTTPError as err:
        raise HTTPError("Error code: {}".format(err.code))

    return res


def extract_input(in_str: str) -> (str, str):
    # Like Queens,NY
    reg = "([A-Za-z -]+),([A-Za-z ]{2})$"
    res = re.search(reg, in_str)

    if res is not None:
        return res.group(1), res.group(2)

    return "", ""


def print_banner() -> None:
    with open("graphic/home_banner.txt") as f:
        for line in f.readlines():
            print(line, end="")

    print("\n\n\n")


def clear() -> None:
    print("\u001b[2J")


def clear_and_print_banner() -> None:
    clear()
    print_banner()


def main(args: list[str]) -> None:
    pass


if __name__ == '__main__':

    main([])
    clear_and_print_banner()
