# Project-0-Python
## Weather App

### This app is a Python implementation of the weather reporting & forecasting app from Project-0.
It also comes with several enhancements:
* Weather alert reporting system
* Ease of configuration for developers. You can perform a decent amount of customization on `config.py` to adapt the application to your needs.

This app uses the OpenWeather API's One-Call API endpoint to get weather data from any U.S. city.

### Functionalities
1) Reports current weather, temperature & other meteorological data for the requested city.
2) Plots a scatter graph of the 60-minute forecast of precipitation in the city.
3) Plots a scatter graph of the hourly forecast of temperature in the city for the next 24 hours & prints a summarized report.
4) Displays the weather forecast of the city for the next 7 days & prints a summarized report.
5) Weather alert reports (if any)

### Technology
* Python 3.9
* Tabulate 0.8.9
* Plotext 3.1.3
* Numpy 1.21.2
* Termcolor 1.1.0

### Usage
After cloning the repository, navigate to the project's root directory.

#### Installing the required packages
You can automatically install the necessary dependencies with `pip` by doing `pip install -r requirements.txt`

#### Adding your own OpenWeather API key
If you don't have one already, you can sign-up for a free API key for testing purposes at https://openweathermap.org/api.
Once you have your own API key, you only need to assign to the `API_KEY` variable in `config.py`

You're all set! To run the application, do `python main.py`.

