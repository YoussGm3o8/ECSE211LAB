"""
main.py
"""

from components import ultrasonic
from components.gyrosensor import g_sensor
import components.navigation as nav
from components.navigation import wheel_left, wheel_right
from components.ultrasonic import us_sensor
from components.colorsensor import color_sensor, left_color_sensor

# g_sensor is the gyrosensor. Use g_sensor.fetch() to get data

# us_sensor is the ultrasonic sensor use us_sensor.fetch() to get data

# color_sensor is the color sensor use color_sensor.fetch() to get data (NOTE: I will create color_sensor.predict() eventually)

# nav is a file with methods defined in it (Not an object like the ones above)

#if you need more sensors look at the files imported to see how each sensor was initiated

sensor_claw_distance = 3
sensor_side_distance = 1

from utils.brick import Motor, EV3UltrasonicSensor, wait_ready_sensors
import time

WHEEL_ACTION = {"backwards" : [180, 180], "forwards" : [-180, -180],
                "right" : [-90, 90], "left" : [90, -90]}

ultra_front = EV3UltrasonicSensor(1) # port S1
#ultra_side = EV3UltrasonicSensor(2) # port S2
sensor_claw_distance = 3
sensor_side_distance = 1

wait_ready_sensors()

wheel_left.set_dps(0)
wheel_right.set_dps(0)


def get_front_distance():
    return (ultra_front.get_value())

def get_side_distance():
    return (ultra_side.get_value())

#action can be forwards, backwards, left, right

    
def correct_direction(degrees):
    if degrees < -1:
        turn_right()
    if degrees > 1:
        turn_left()
    else:
        pass
    
def main():
    current_direction = g_sensor.fetch()
    while True:
        print(get_front_distance())
        activate_wheels("forwards")
        if get_front_distance() < 10 :
            time.sleep(1)
            stop_wheels()
            # TODO add detect cube color and pickup here or something
        if get_front_distance() < 15 : # this should be changed to internally calculate how far the robot moves,
                                       #measure wheel diameter and rotations per second, get distance/second aka speed in cm.
            print(get_front_distance())
            stop_wheels()
            while current_direction < 90 :
                turn_right()
                current_direction = g_sensor.fetch()
            current_direction = 0
        correct_direction(g_sensor.fetch())
