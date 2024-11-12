"""
main.py
"""
from utils.brick import EV3UltrasonicSensor, wait_ready_sensors, reset_brick
import time

from components import ultrasonic
from components.gyrosensor import g_sensor
import components.navigation as nav
from components.navigation import wheel_left, wheel_right
from components.ultrasonic import us_sensor
from components.colorsensor import color_sensor

# g_sensor is the gyrosensor. Use g_sensor.fetch() to get data

# us_sensor is the ultrasonic sensor use us_sensor.fetch() to get data

# color_sensor is the color sensor use color_sensor.fetch() to get data (NOTE: I will create color_sensor.predict() eventually)

# nav is a file with methods defined in it (Not an object like the ones above)

#if you need more sensors look at the files imported to see how each sensor was initiated

sensor_claw_distance = 3
robot_length = 10



ultra_front = EV3UltrasonicSensor(1) # port S1
#ultra_side = EV3UltrasonicSensor(2) # port S2
sensor_claw_distance = 3
#sensor_side_distance = 1

wait_ready_sensors()

wheel_left.set_dps(0)
wheel_right.set_dps(0)


def get_front_distance():
    return (ultra_front.get_value())

#def get_side_distance():
#   return (ultra_side.get_value())

#action can be forwards, backwards, left, right

    
def correct_direction(degrees):
    if degrees < -10:
        nav.turn_right()
    if degrees > 10:
        nav.turn_left()
    else:
        pass
    
def main():
    new_angle = 0
    moving_f = True
    try:

        while True:       
            nav.activate_wheels("forwards")
            while True:
                d = get_front_distance()
                print(d)
                if d < 15:
                    break
                time.sleep(0.05)
                c = color_sensor.predict()

                print(c)
                if c == 'b':
                    nav.stop_wheels()
                    nav.activate_wheels("right")
                    while c == 'b':
                        c = color_sensor.predict()
                        print(c)
                        if c != 'b':
                            break
                    nav.stop_wheels()
                    nav.activate_wheels("forwards")
                    


        
            if get_front_distance() < 15 : # this should be changed to internally calculate how far the robot moves,
                    print(get_front_distance())
                    nav.stop_wheels()
                    # TODO add detect cube color and pickup here or something
                    
                    while (((g_sensor.fetch() - new_angle) % 360) < 90) :
                        nav.turn_right()
                    new_angle = g_sensor.fetch()
            
            correct_direction(g_sensor.fetch())
    finally:
        reset_brick()
        
        
if __name__ == "__main__":
    main()
