import time

from common.polling import poll
from components.gyrosensor import g_sensor
from components.ultrasonic import us_sensor
import csv
from utils.brick import Motor, wait_ready_sensors

# Constants
SLOW = 90
MODERATE = 180
FAST = 360

WHEEL_ACTION = {
    "backwards": [180, 180],
    "forwards": [-180, -180],
    "right": [-90, 90],
    "left": [90, -90],
}

LEFT_WHEEL_PORT = "C"
RIGHT_WHEEL_PORT = "B"

WHEEL_TO_CAR_DEGREE_RATIO = 1.9722

# Components

wheel_left = Motor(LEFT_WHEEL_PORT)
wheel_right = Motor(RIGHT_WHEEL_PORT)

arm = Motor("A")

# functions

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
    arm.set_limits(0, 360)
    arm.set_position_relative(degrees)


def set_limits(dps):
    wheel_left.set_limits(0, dps)
    wheel_right.set_limits(0, dps)


def rotate(speed, stop_angle):
    """
    scan front of car to detect objects
    """
    sign = -1 if stop_angle < 0 else 1
    stop_angle = abs(stop_angle)
    angle = poll(g_sensor.fetch)
    turn(speed * sign)
    _angle = sign * (poll(g_sensor.fetch) - angle)
    while _angle < stop_angle:
        _angle = sign * (poll(g_sensor.fetch) - angle)
        print(_angle)
        continue
    stop()
