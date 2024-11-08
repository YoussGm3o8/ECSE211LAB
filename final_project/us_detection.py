from utils.brick import EV3UltrasonicSensor

# Constants

US_SENSOR_PORT = 1

# Components

us_sensor = EV3UltrasonicSensor(US_SENSOR_PORT)

#Functions

def get_distance():
    return us_sensor.get_value()


