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

#CONSTANTS

TIMEOUT = 10

SLOW = 90
MODERATE = 180
FAST = 360

#apply median filter to sensor with a window of 10
us_sensor = Filtered_Sensor(us_sensor, Median_Filter(10))
#NOTE: the other sensors are called g_sensor and color_sensor (they are already initialized)



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
try:
    while True:
        speed = FAST
        nav.forward(speed)
        while True:

            #DISTANCE
            dist = us_sensor.fetch()
            if dist is None:
                print("dist is None")
                nav.stop()
                dist = wait_for(us_sensor.fetch)
                nav.forward(speed)
                print("dist is not None")

            if dist < 30:
                break

            #COLOR
            color = color_sensor.fetch()
            if color is None:
                print("color None")
                nav.stop()
                color = wait_for(color_sensor.fetch)
                nav.forward(speed)
                print("color not None")

            if color == 'b':
                print("color is b")
                nav.stop()
                g_sensor.reset_measure()
                nav.turn(SLOW)
                print(g_sensor.fetch(), "is 0")

                while True:
                    angle = g_sensor.fetch()
                    if angle is None:
                        nav.stop()
                        angle = wait_for(g_sensor.fetch)
                        nav.turn(SLOW)
                        print(angle)
                    if abs(angle) > 89:
                        nav.stop()
                        break

        #at this point the car is near something
        nav.stop()
        #turn 90 degrees
        g_sensor.reset_measure()
        nav.turn(SLOW)
        while True:
            dist = us_sensor.fetch()
            if dist is None:
                print("dist None")
                nav.stop()
                dist = wait_for(us_sensor.fetch)
                nav.turn(SLOW)
                print("dist not None")

            angle = g_sensor.fetch()
            if angle is None:
                nav.stop()
                angle = wait_for(g_sensor.fetch)
                nav.turn(SLOW)
            if abs(angle) > 89 and dist > 40:
                nav.stop()
                break

finally:
    reset_brick()
