from utils.brick import Motor
from utils.brick import wait_ready_sensors
# Constants

LEFT_WHEEL_PORT = "C"
RIGHT_WHEEL_PORT = "B"

WHEEL_TO_CAR_DEGREE_RATIO = 1.9722

# Components

lwheel = Motor(LEFT_WHEEL_PORT)
rwheel = Motor(RIGHT_WHEEL_PORT)

# functions


def forward(dps):
    """
    continuously go forward

    Arguments:
        dps: degrees per seconds
    """
    lwheel.set_dps(dps)
    rwheel.set_dps(dps)


def move_forward(degrees, dps, convertion=False):
    """
    Move a the wheels a number of degrees (making the car go either forward [DEFAULT] or backwards)

    Argument:
        degrees: number of degrees to turn wheels
        dps: degrees per second
        convertion: if True, degrees will be converted to car degrees (360 => 1 car turn)
    """
    if not convertion:
        lwheel.set_limits(0, dps)
        rwheel.set_limits(0, dps)
        rwheel.set_position_relative(degrees)
        lwheel.set_position_relative(degrees)
    else:
        degrees *= WHEEL_TO_CAR_DEGREE_RATIO
        lwheel.set_limits(0, dps)
        rwheel.set_limits(0, dps)
        rwheel.set_position_relative(degrees)
        lwheel.set_position_relative(degrees)


def keep_left(dps):
    """
    continuously rotate the car left

    Arguments:
        dps: degrees per seconds

    NOTE: negative degrees will make the car turn right
    """

    lwheel.set_dps(-dps)
    rwheel.set_dps(dps)


def turn_left(degrees, dps, convertion=False):
    """
    Similar to keep_left but once the car is in motion it cannot be stopped

    Arguments:
        degree: the wheels will rotate this number of degrees
        dps: degrees per seconds
        convertion: if True, degrees will be converted to car degrees (360 => 1 car turn)

    NOTE: negative degrees will make the car turn right
    """
    if not convertion:
        lwheel.set_limits(0, dps)
        rwheel.set_limits(0, dps)
        lwheel.set_position_relative(-degrees)
        rwheel.set_position_relative(degrees)
    else:
        degrees *= WHEEL_TO_CAR_DEGREE_RATIO
        lwheel.set_limits(0, dps)
        rwheel.set_limits(0, dps)
        lwheel.set_position_relative(-degrees)
        rwheel.set_position_relative(degrees)
