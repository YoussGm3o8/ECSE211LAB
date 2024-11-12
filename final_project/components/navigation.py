from utils.brick import Motor
from utils.brick import wait_ready_sensors
import time
# Constants

WHEEL_ACTION = {"backwards" : [180, 180], "forwards" : [-180, -180],
                "right" : [-180, 180], "left" : [180, -180]}

LEFT_WHEEL_PORT = "C"
RIGHT_WHEEL_PORT = "D"

WHEEL_TO_CAR_DEGREE_RATIO = 1.9722

# Components

wheel_left = Motor(LEFT_WHEEL_PORT)
wheel_right = Motor(RIGHT_WHEEL_PORT)

# functions

def activate_wheels(action):
    wheel_left.set_dps(WHEEL_ACTION.get(action)[0]);
    wheel_right.set_dps(WHEEL_ACTION.get(action)[1]);

def stop_wheels():
    wheel_left.set_dps(0)
    wheel_right.set_dps(0)

#turns right for 0.1 seconds
def turn_right():
    activate_wheels("right")
    time.sleep(0.1)
    stop_wheels()

#turns left for 0.1 seconds
def turn_left():
    activate_wheels("left")
    time.sleep(0.1)
    stop_wheels()