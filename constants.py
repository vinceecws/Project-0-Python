EXCLUDE_OPTS = {"current", "minutely", "hourly", "daily", "alerts"}
WIND_DEG_QUADRANT = {
    0: "N",
    1: "NE",
    2: "E",
    3: "SE",
    4: "S",
    5: "SW",
    6: "W",
    7: "NW"
}
UNITS_ALL = {
    "pressure": "hPa",
    "humidity": "%",
    "clouds": "%",
    "visibility": {
        "low": "m",
        "high": "km"
    },
    "wind_deg": {
        "N": "° N",
        "S": "° S",
        "E": "° E",
        "W": "° W",
        "NE": "° NE",
        "NW": "° NW",
        "SE": "° SE",
        "SW": "° SW",
    },
    "pop": "%",
    "rain": "mm/h",
    "snow": "mm/h",
    "precipitation": "mm/h"
}
UNITS_IMPERIAL = {
    "temp": "°F",
    "feels_like": "°F",
    "dew_point": "°F",
    "wind_speed": "mph",
    "wind_gust": "mph"
}
