from utils.brick import Motor
from utils.brick import wait_ready_sensors
import time
# Constants

WHEEL_ACTION = {"backwards" : [180, 180], "forwards" : [-180, -180],
                "right" : [-90, 90], "left" : [90, -90]}

LEFT_WHEEL_PORT = "C"
RIGHT_WHEEL_PORT = "B"

WHEEL_TO_CAR_DEGREE_RATIO = 1.9722

# Components

wheel_left = Motor(LEFT_WHEEL_PORT)
wheel_right = Motor(RIGHT_WHEEL_PORT)

arm = Motor("A")

# functions

def activate_wheels(action):
    wheel_left.set_dps(2 * WHEEL_ACTION.get(action)[0])
    wheel_right.set_dps(2 * WHEEL_ACTION.get(action)[1])

def stop_wheels():
    wheel_left.set_dps(0)
    wheel_right.set_dps(0)

#turns right for 0.05 seconds
def turn_right():
    activate_wheels("right")
    time.sleep(0.05)
    stop_wheels()

#turns left for 0.1 seconds
def turn_left():
    activate_wheels("left")
    time.sleep(0.1)
    stop_wheels()

#hand Motor and hatch Motor relocated to objects.py

def stop():
    wheel_left.set_dps(0)
    wheel_right.set_dps(0)

def forward(dps):
    """
    move forward continuously
    MAX: 1250 degree per seconds
    """
    wheel_left.set_dps(-dps)
    wheel_right.set_dps(-dps)

def turn(dps):
    """
    turn left continuously
    MAX: 1250 degree per seconds
    """
    wheel_left.set_dps(dps)
    wheel_right.set_dps(-dps)

def move_arm(degrees):
    arm.reset_position()
    arm.set_limits(0,180)
    arm.set_position_relative(degrees)

def set_limits(dps):
    wheel_left.set_limits(0, dps)
    wheel_right.set_limits(0, dps)

