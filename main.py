import sys

from urllib.error import HTTPError
from termcolor import colored
from weather.weather_data import WeatherData
from util import get_geo, get_weather, extract_input, clear, clear_and_print_banner


def main() -> None:
    while True:
        clear_and_print_banner()

        while True:
            place = input(colored("Which city's weather would you like to see? " +
                                  "Input as: city,state\n" +
                                  "Or, press Q to exit: ", attrs=["bold"]))

            if place.lower() == "q":
                sys.exit()

            city_state = extract_input(place)

            try:
                lat_lon = get_geo(city_state[0], city_state[1])
            except HTTPError:
                print(colored("Oh no! API server is not responding. " +
                              "Maybe out of quota?", "red", attrs=["bold"]))
                print("Application will exit now...")
                sys.exit()

            if lat_lon is not None:
                break

            print(colored("\n There does not seem to be any good matches to your search. " +
                          "Try something like: Queens,NY",
                          attrs=["bold"]))

        try:
            weather = get_weather(lat_lon["lat"], lat_lon["lon"])
        except HTTPError:
            print(colored("Oh no! API server is not responding. " +
                          "Maybe out of quota?", "red", attrs=["bold"]))
            print("Application will exit now...")
            sys.exit()

        weather_data = WeatherData(weather, lat_lon["city"], lat_lon["state"])

        while True:
            clear_and_print_banner()
            weather_data.current.print_report()

            if weather_data.alerts is not None:
                print()
                weather_data.alerts.print_report()

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
                sys.exit()
            else:
                print(colored("Invalid selection.", "red"))

            print()
            input(colored("Press ENTER to go back: ", attrs=["bold"]))


if __name__ == '__main__':
    main()
