from utils.brick import Motor
import time
# functions
hand = Motor("C")

def wait_for(func):
    """
    Wait for a function to return a value
    """
    v = func()
    while v is None:
        v = func()
    return v


def init_hand():
    """
    Don't know if this works but supposed to set the hand to a known position and reset the encoder there
    """
    hand.set_power(-5)
    speed = wait_for(hand.get_speed)
    while speed > -5:
        speed = wait_for(hand.get_speed)
    hand.set_power(0)
    hand.reset_encoder()

def pickup_cube():
    """
    Pickup a cube (Not tested)
    """
    hand.set_position(360)
    time.sleep(0.5)
    hand.set_position(0)


hatch = Motor("A") #TODO: fix this motor

