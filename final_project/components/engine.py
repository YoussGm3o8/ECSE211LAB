"""
Initialization of devices and threads into one file

To use the devices you have to poll the variables in the global_state list

Usage:

    #global_state is a list of the current state of sensors

    global_state = {us_sensor, color_sensor1, color_sensor2, g_sensor, ...}

    PLEASE DEFINE ADDTIONAL SENSORS IF NEEDED (ADD TO THE LIST ABOVE AT '...')

    color_sensor1 and color_sensor2 are colors from the following: {'r, 'o', 'g', 'p', 'b', 'y', 'unknown', None}

    us_sensor is a float of the distance in cm

    g_sensor is a float of the angle in degrees from start of the program (it can be above 360 or below 0 e.g. 370 or -1012)


NOTES: make sure that the main loop is faster than the polling rate of sensor (the queue blocks when full)
"""

import time
from components.gyrosensor import g_sensor
from components.ultrasonic import us_sensor as rus_sensor
from components.colorsensor import color_sensor, color_sensor2
from common.wrappers import Filtered_Sensor_V2, US_Sensor_High_PollingRate, US_Sensor_High_PollingRate_V2
from common.filters import Median_Filter
from common import threads
from queue import Queue
from collections import namedtuple
from utils.brick import reset_brick

#state is a named tuple that stores the current state of the sensors
#example usage 1: state.us_sensor -> gives the value of the us_sensor
#example usage 2: state.color_sensor -> gives the value of the color_sensor
state = namedtuple("state", ["us_sensor", "color_sensor", "color_sensor2", "g_sensor", "raw_us_sensor"])

global_state = Queue(maxsize=2)
us_sensor = Filtered_Sensor_V2(rus_sensor, Median_Filter(5))
th_engine = threads.ThreadEngine()

def start():
    global us_sensor
    # us_sensor = US_Sensor_High_PollingRate_V2(Filtered_Sensor_V2(rus_sensor, Median_Filter(5))) #this this approach with follow_gradient_V2
    us_sensor = Filtered_Sensor_V2(US_Sensor_High_PollingRate(rus_sensor), Median_Filter(5))
    th_engine.loop(poll_sensors)

def end():
    th_engine.join_all()
    reset_brick()

def get_state():
    fus, rus = us_sensor.fetch()
    return state(
        fus, 
        color_sensor.fetch(),
        color_sensor2.fetch(), 
        g_sensor.fetch(),
        rus)

def poll_sensors():
    """
        for idx look at common/logging.py
    """
    global_state.put(get_state())
    time.sleep(0.05)
