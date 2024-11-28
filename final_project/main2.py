import subsystem.car as car
import time
from common.constants_params import *

car = car.Car()

columns = 6

try:
    for i in range(columns):
        direction = 1 if i % 2 == 0 else -1
        car.forward(MODERATE, 120)       
        angle = car.abs_angle_time
        while not car.is_stopped:
            car.avoid_water()
            if car.detect_objects(7):
                print("pickup the object")
                #make a prompt that wait for the user to press enter
                car.stop()
                input("Press Enter to continue...")
                car.previous_action()

            car.fix_angle(angle)
            car.update()
            time.sleep(0.05)
        car.reverse(MODERATE, 10)
        car.wait_for_action()
        if direction == 1:
            car.turn_left(MODERATE, 50)
            car.wait_for_action()
        else:
            car.turn_right(MODERATE, 50)
            car.wait_for_action()
        #add some avoid_water condition here
        car.forward(MODERATE, 15)
        angle = car.abs_angle_time
        while not car.is_stopped:
            time.sleep(0.05)
            car.update()
            car.avoid_water()
            car.fix_angle(angle)

        if direction == 1:
            car.turn_left(MODERATE, 50)
            car.wait_for_action()
        else:
            car.turn_right(MODERATE, 50)
            car.wait_for_action()

    car.reverse(MODERATE, 10)
    car.wait_for_action()
    car.turn_left(MODERATE, 180)
    car.wait_for_action()
    car.forward(MODERATE, 120)
    car.wait_for_action() #in theory you are done (if you did not hit the lake which is impossible)
finally:
    car.kill()