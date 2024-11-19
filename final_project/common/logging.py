from collections import deque

"""
Global state for devices (used to interact between threads)

usage:
global_state = {us_sensor, color_sensor1, color_sensor2, g_sensor, ...}
PLEASE DEFINE ADDTIONAL SENSORS IF NEEDED (ADD TO THE LIST ABOVE AT '...')
"""
global_state = [None, None, None, None]

global_flags = deque(maxlen=10) #we will use this queue for flags/errors


