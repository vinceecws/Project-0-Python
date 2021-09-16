import json
import re
import urllib.request as request
import urllib.parse as parse

from config import *
from constants import *
from weather.weather_data import WeatherData
from typing import Any
from termcolor import colored
from urllib.error import HTTPError


def get_geo(city: str, state: str, limit: int = 10) -> dict[str, str]:
    city = parse.quote(city)
    state = parse.quote(state)

    url = parse.urljoin(BASE_URL, GEO_ENDPOINT) + \
          f"?q={city},{state},US&limit={limit}&appid={API_KEY}"
    try:
        res = json.loads(request.urlopen(url).read())
    except HTTPError as err:
        raise HTTPError(f"Error code: {err.code}")

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
        else:
            url = parse.urljoin(BASE_URL, WEATHER_ENDPOINT) + \
                  f"?lat={lat}&lon={lon}&exclude={exclude}&appid={API_KEY}&units={UNITS}"
    else:
        url = parse.urljoin(BASE_URL, WEATHER_ENDPOINT) + \
              f"?lat={lat}&lon={lon}&appid={API_KEY}&units={UNITS}"

    try:
        res = json.loads(request.urlopen(url).read())
    except HTTPError as err:
        raise HTTPError(f"Error code: {err.code}")

    return res


def extract_input(in_str: str) -> (str, str):
    # Like Queens,NY
    reg = "([A-Za-z -]+),([A-Za-z ]{2})$"
    res = re.search(reg, in_str.strip())

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


def main() -> None:
    while True:
        clear_and_print_banner()

        while True:
            place = input(colored("Which city's weather would you like to see? Input as: city,state\n" +
                                  "Or, press Q to exit: ", attrs=["bold"]))

            if place.lower() == "q":
                exit()

            city_state = extract_input(place)

            try:
                lat_lon = get_geo(city_state[0], city_state[1])
            except HTTPError as err:
                print(colored("Oh no! API server is not responding. Maybe out of quota?", "red", attrs=["bold"]))
                print("Application will exit now...")
                exit()

            if lat_lon is not None:
                break

            print(colored("\n There does not seem to be any good matches to your search. Try something like: Queens,NY",
                          attrs=["bold"]))

        try:
            weather = get_weather(lat_lon["lat"], lat_lon["lon"])
        except HTTPError as err:
            print(colored("Oh no! API server is not responding. Maybe out of quota?", "red", attrs=["bold"]))
            print("Application will exit now...")
            exit()
        print(json.dumps(weather, sort_keys=True, indent=4))
        weather_data = WeatherData(weather, lat_lon["city"], lat_lon["state"])

        while True:
            clear_and_print_banner()
            weather_data.current.print_report()

            print(colored("\nCheck out one of the forecasts:", attrs=["bold"]))
            print("1) Minutely-precipitation for the next 60-minutes")
            print("2) Hourly-weather for the next 24-hours")
            print("3) Daily-weather for the next 7-days")
            print("Or, 4) Try a different city")

            print(colored("\nPress Q to exit: ", attrs=["bold"]))

            selection = input(colored("Your selection: ", attrs=["bold"]))
            clear()
            if selection == "1":
                weather_data.minutely.print_report()
                print("\n")
                weather_data.minutely.plot_data()
            elif selection == "2":
                weather_data.hourly.print_report()
                print("\n")
                weather_data.hourly.plot_data()
            elif selection == "3":
                weather_data.daily.print_report()
                print("\n")
                weather_data.daily.plot_data()
            elif selection == "4":
                break
            elif selection.lower() == "q":
                exit()
            else:
                print(colored("Invalid selection.", "red"))

            print()
            input(colored("Press ENTER to go back: ", attrs=["bold"]))


if __name__ == '__main__':
    main()
