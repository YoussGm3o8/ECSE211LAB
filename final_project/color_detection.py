from utils.brick import EV3ColorSensor

# Constants

COLOR_SENSOR_PORT = 1

# Components

color_sensor = EV3ColorSensor(COLOR_SENSOR_PORT)

# Functions

def get_rgb():
    """
    return [None, None, None] if there is an error
    """
    return color_sensor.get_rgb()