
"""
main.py

DESCRIPTION: A robot that avoids wall and water
"""
from utils.brick import reset_brick
import time
from components.gyrosensor import g_sensor
import components.navigation as nav
from components.ultrasonic import us_sensor
from components.colorsensor import color_sensor
from common.wrappers import Filtered_Sensor
from common.filters import Median_Filter
import csv
import sys
import os
import time


SLOW = 90
MODERATE = 200
FAST = 360

TIMEOUT = 10

#TIMEOUT function
def wait_for(func, *args):
    if not callable(func):
        raise TypeError("func must be a function")
    ti = time.time()
    v = func(*args)
    while v is None:
        v = func(*args)
        if time.time() - ti > TIMEOUT:
            if hasattr(func, '__self__'):
                #this if for debugging purposes
                myclass = func.__self__
                raise TimeoutError(str(myclass)+" not responding...")
            raise TimeoutError("Component not responding...")
    return v

#MAIN LOOP
buffer = []

try:
    nav.turn(MODERATE)
    count = 0
    ti = time.time()
    while True:
        dist = us_sensor.fetch()
        if dist is None:
            nav.stop()
            dist = wait_for(us_sensor.fetch)
            nav.turn(MODERATE)
        buffer.append((count, dist))
        count += 1
        if time.time() - ti > 20:
            break
    nav.stop()
    #write buffer to csv
finally:
    path = os.path.dirname(__file__)
    path = os.path.join(path, "data", "csv")
    with open(os.path.join(path, "us_data.csv"), "w") as f:
        writer = csv.writer(f)
        writer.writerows(buffer)
    reset_brick()
