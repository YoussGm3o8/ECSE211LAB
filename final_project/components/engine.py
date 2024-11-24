"""
This file is used to easily poll the sensors using threads

Example usage:
    import engine

    engine.start()

    try:
        while True:
            state = engine.poll_state()

            if state.us_sensor is not None:
                print(state.us_sensor)

            if state.color_sensor is not None:
                print(state.color_sensor)

            if state.color_sensor2 is not None:
                print(state.color_sensor2)

            if state.g_sensor is not None:
                print(state.g_sensor)
    finally:
        engine.end() #make sure to call this function to end the threads and reset the brick


    Alternatively you can use the engine.get_state() function to get the state of the sensors without using threads.
    In this case you don't call engine.start() (still use engine.end() to stop the brickpi).
"""

import time
from components.gyrosensor import g_sensor
from components.ultrasonic import us_sensor
from components.colorsensor import color_sensor, color_sensor2
from common.wrappers import Filtered_Sensor
from common.filters import Median_Filter
from common import threads
from queue import Queue
from collections import namedtuple
from utils.brick import reset_brick

#state is a named tuple that stores the current state of the sensors
#example usage 1: state.us_sensor -> gives the value of the us_sensor
#example usage 2: state.color_sensor -> gives the value of the color_sensor
state = namedtuple("state", ["us_sensor", "color_sensor", "color_sensor2", "g_sensor"])

global_state = Queue(maxsize=2)

us_sensor = Filtered_Sensor(us_sensor, Median_Filter(5))
th_engine = threads.ThreadEngine()

def poll_state():
    """
    Use this function to obtain the state of the sensors using threads

    NOTE: polling the sensors will lead to frequent None values for the color sensors therefore you must check for None values
    """
    try:
        colors = global_state.get_nowait()
    except Exception:
        colors = [None, None]
    return state(
    us_sensor.fetch(),
    colors[0],
    colors[1],
    g_sensor.fetch()
    )

def get_state():
    """
    if you don't want to use threads you can use this function instead
    """
    return state(
    us_sensor.fetch(),
    color_sensor.fetch(),
    color_sensor2.fetch(),
    g_sensor.fetch()
    )

def poll_sensors():
    """
    Only polls the color_sensors since they require a delay between each fetch
    """
    global_state.put((color_sensor.fetch(), color_sensor2.fetch()))
    time.sleep(0.05)


def start():
    th_engine.loop(poll_sensors)

def end():
    th_engine.join_all()
    reset_brick()

