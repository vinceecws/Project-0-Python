import datetime
from constants import *

LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
API_KEY = "YOUR OPENWEATHER API KEY"
UNITS = "imperial"
BASE_URL = "http://api.openweathermap.org/"
GEO_ENDPOINT = "/geo/1.0/direct"
WEATHER_ENDPOINT = "/data/2.5/onecall"
PLOT_SIZE_X = 100
PLOT_SIZE_Y = 20

# Plot graphical configs. If set to None, use default.
# Available options here: https://github.com/piccolomo/plotext#plot-aspect
PLOT_CANVAS_COLOR = "white"
PLOT_AXES_COLOR = "teal"
PLOT_TICKS_COLOR = "blue"
PLOT_MARKER_1 = "smile"
PLOT_MARKER_2 = "heart"

# Config parameters checking
assert UNITS in UNITS_LIB, f"Invalid unit system. Must be one of {list(UNITS_LIB.keys())}"
assert PLOT_SIZE_X > 0 and PLOT_SIZE_Y > 0, \
    f"Invalid plot sizes of PLOT_SIZE_X (width)={PLOT_SIZE_X}, PLOT_SIZE_Y (height)={PLOT_SIZE_Y}. Both must be > 0."
