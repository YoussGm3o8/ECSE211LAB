"""
initialization of devices
"""
import time
from components.gyrosensor import g_sensor
from components.ultrasonic import us_sensor
from components import colorsensor
from common.wrappers import Filtered_Sensor
from common.filters import Median_Filter
from common.logging import global_state, global_flags

from common import threads
#CONSTANTS

TIMEOUT = 10

SLOW = 90
MODERATE = 180
FAST = 360

#apply median filter to sensor with a window of 10
us_sensor = Filtered_Sensor(us_sensor, Median_Filter(10))
color_sensor2 = colorsensor.Color_Sensor2(2)

th_engine = threads.ThreadEngine()


def poll_sensor(sensor, idx):
    """
        for idx look at common/logging.py
    """
    value = sensor.fetch()
    while value is None:
        value = sensor.fetch()
        global_state[idx] = value #poll faster when the sensor is not responding

    global_state[idx] = value
    time.sleep(0.05) #the function is looped  therefore make sure we do not poll the device too frequently when its functional


th_engine.loop(poll_sensor, us_sensor, 0) 

