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
"""

import time
from components.gyrosensor import g_sensor
from components.ultrasonic import us_sensor
from components.colorsensor import color_sensor, color_sensor2
from common.wrappers import Filtered_Sensor
from common.filters import Median_Filter
from common import threads

global_state = {"us_sensor":None, "color_sensor": None, "color_sensor2": None, "g_sensor": None}
global_enable = [True]*4 #enable/disable sensors in the order of above initialization

us_sensor = Filtered_Sensor(us_sensor, Median_Filter(10))

th_engine = threads.ThreadEngine()

def poll_sensors():
    """
        for idx look at common/logging.py
    """

    if global_enable[0]:
        global_state["us_sensor"] = us_sensor.fetch()

    if global_enable[1]:
        global_state["color_sensor"] = color_sensor.fetch()

    if global_enable[2]:
        global_state["color_sensor2"] = color_sensor2.fetch()

    if global_enable[3]:
        global_state["g_sensor"] = g_sensor.fetch()

    time.sleep(0.05)

def start():
    th_engine.loop(poll_sensors)

def end():
    th_engine.join_all()

