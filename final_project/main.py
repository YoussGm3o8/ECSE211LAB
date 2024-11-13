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
from components.wrappers import Filtered_Sensor
from common.filters import Median_Filter

#CONSTANTS

TIMEOUT = 10

SLOW = 90
MODERATE = 180
FAST = 360

#apply median filter to sensor with a window of 10
us_sensor = Filtered_Sensor(us_sensor, Median_Filter(10))
#NOTE: the other sensors are called g_sensor and color_sensor (they are already initialized)



#TIMEOUT function
def wait_for(func):
    if not callable(func):
        raise TypeError("func must be a function")
    ti = time.time()
    v = func()
    while v is None:
        v = func()
        if time.time() - ti > TIMEOUT:
            if hasattr(func, '__self__'):
                #this if for debugging purposes
                myclass = func.__self__
                raise TimeoutError(str(myclass)+" not responding...")
            raise TimeoutError("Component not responding...")
    return v


#MAIN LOOP
try:
    speed = FAST
    while True:
        nav.forward(speed)
        while True:

            #DISTANCE
            dist = us_sensor.fetch()
            if dist is None:
                nav.stop()
                dist = wait_for(us_sensor.fetch)
                nav.forward(speed)

            if dist >= 30:
                speed = FAST
            else:
                speed = MODERATE

            if dist < 15:
                break

            #COLOR
            color = color_sensor.fetch()
            if color is None:
                nav.stop()
                color = wait_for(color_sensor.fetch)
                nav.forward(speed)

            if color == 'b':
                nav.stop()
                g_sensor.reset_measure()
                g_sensor.wait_ready()
                nav.turn(SLOW)

                while True:
                    angle = g_sensor.fetch()
                    if angle is None:
                        nav.stop()
                        angle = wait_for(g_sensor.fetch)
                        nav.turn(SLOW)
                    if abs(angle) > 88:
                        nav.stop()
                        break

        #at this point the car is near something
        nav.stop()
        #turn 90 degrees
        g_sensor.reset_measure()
        g_sensor.wait_ready()
        nav.turn(SLOW)
        while True:
            dist = us_sensor.fetch()
            if dist is None:
                nav.stop()
                dist = wait_for(us_sensor.fetch)
                nav.turn(SLOW)

            angle = g_sensor.fetch()
            if angle is None:
                nav.stop()
                angle = wait_for(g_sensor.fetch)
                nav.turn(SLOW)
            if abs(angle) > 88 and dist > 40:
                nav.stop()
                break

finally:
    reset_brick()
