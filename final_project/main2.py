import subsystem.car as car
import time
from common.constants_params import *
from common.filters import Diff



TURN_SPEED = 150
FORWARD_SPEED = 210
TIMER = 120

car = car.Car(debug=False)

def avoid_water(car):
    water_f = car.is_water()
    if water_f[0] == True:
        car.turn_right(TURN_SPEED)
        while water_f[0] == True:
            car.update(0.05)
            water_f = car.is_water()
        time.sleep(0.1)
        car.forward(FORWARD_SPEED)
    if water_f[1] == True:
        car.turn_left(TURN_SPEED)
        while water_f[1] == True:
            car.update(0.05)
            water_f = car.is_water()
        time.sleep(0.1) #important to overturn
        car.forward(FORWARD_SPEED)

def check_cube(car):
    # always detects wall next to cube...
    # if car.avoid_wall(8):
    #     print("wall detected next to cube")
    #     return
    car.update(0.05)
    object = car.mini_scan()
    if object[0] is not None:
        if object[1] == "o" or object[1] == "y":
            print("cube color detected ", object[1], "at sensor ", object[0])
            car.stop()
            # print(object)
            # input("press any to continue")
            car.collect_cube()
            # car.forward(FORWARD_SPEED)
        else:
            print("cube color detected avoiding ", object[1], "at sensor ", object[0])
            avoiding = car.avoid_wall(25)
            if avoiding[0]:
                if avoiding[1] == "right":
                    car.turn_left(TURN_SPEED, 10)
                    car.wait_for_action()
                elif avoiding[1] == "left":
                    car.turn_right(TURN_SPEED, 10)
                    car.wait_for_action()
                elif avoiding[1] == "front":
                    car.turn_right(TURN_SPEED, 20)
                    car.wait_for_action()
            else:
                car.turn_right(TURN_SPEED, 5)
                car.wait_for_action()

clock = 0
def scan(car, duration=8, treshold=25):
    if clock % 14 == 0:
        print("---------------scanning ---------------")

        car.turn_left(TURN_SPEED)
        for i in range(duration):
            check_cube(car)
            check_wall(car)
            avoid_water(car)

        car.turn_right(TURN_SPEED)
        for i in range(duration*2):
            check_cube(car)
            check_wall(car)
            avoid_water(car)

        car.turn_left(TURN_SPEED)
        for i in range(duration):
            check_cube(car)
            check_wall(car)
            avoid_water(car)

        car.forward(FORWARD_SPEED)
    else:
        check_cube(car)
        car.forward(FORWARD_SPEED)


def check_wall(car):
    avoiding = car.avoid_wall(10)
    if avoiding[0]:
        print("wall detected", avoiding[1])

        if avoiding[1] == "front":
            car.reverse(FORWARD_SPEED, 5)
            car.wait_for_action()
            car.turn_right(TURN_SPEED, 20)
            while not car.is_stopped:
                car.update(0.05)
                avoid_water(car)
                if not car.avoid_wall(8)[0]:
                    time.sleep(0.2)
                    break


        elif avoiding[1] == "right":
            print("turn left for right wall")
            car.turn_left(TURN_SPEED, 20)
            while not car.is_stopped:
                car.update(0.05)
                avoid_water(car)
                if not car.avoid_wall(8)[0]:
                    time.sleep(0.2)
                    break
        else:
            print("turn right for left wall")
            car.turn_right(TURN_SPEED, 20)
            while not car.is_stopped:
                car.update(0.05)
                avoid_water(car)
                if not car.avoid_wall(8)[0]:
                    time.sleep(0.2)
                    break
        car.forward(FORWARD_SPEED)


def rotate(car, sp=20):
    while True:
        car.update(0.05)
        if car.right_color_sensor.get_base():
            car.stop()
            car.turn_left(TURN_SPEED, 70)
            car.wait_for_action()
            car.reverse(100, 7)
            car.wait_for_action()
            car.dump_cubes()
            print("success! hopefully...")
            exit()
        if car.state.us_sensor > sp:
            car.wheel_right.set_dps(FORWARD_SPEED + 100)
            car.wheel_left.set_dps(FORWARD_SPEED)
            while car.state.us_sensor > sp:
                car.update(0.05)
            car.turn_left(TURN_SPEED)


def return_home(car):
    """
    assume you are at a border facing the wall
    """
    sp = 20
    car.forward(FORWARD_SPEED)
    while True:
        car.update(0.05)
        avoid_water(car)
        if (car.state.us_sensor < 14 or car.state.us_sensor_2 < 14):
            break
    if car.state.us_sensor < 15:
        rotate(car, sp)
    else:
        car.turn_right(TURN_SPEED)
        while True:
            if car.state.us_sensor < 25:
                car.stop()
                break
            car.update(0.05)
        rotate(car, sp)

try:
    ti = time.time()
    car.forward(FORWARD_SPEED)
    while True:
        clock += 1
        if time.time() - ti > TIMER:
            print("time to return home!")
            break
        print("flag: ", car.flag)
        car.update(0.025)
        check_wall(car)
        avoid_water(car)
        scan(car)
    print("returning home")
    return_home(car)
finally:
    car.kill()

# def scan(car, duration=10):
#     if car.clock % 100 == 0:
#         print("scanning ---------------")
#         car.turn_left(100)
#         for i in range(duration):
#             car.update(0.05)
#             check_cube(car)
#             avoid_water(car)
#         car.turn_right(100)
#         for i in range(duration*2):
#             car.update(0.05)
#             check_cube(car)
#             avoid_water(car)
#         car.turn_left(100)
#         for i in range(duration):
#             car.update(0.05)
#             check_cube(car)
#             avoid_water(car)
#         car.forward(150)
#     else:
#         check_cube(car)

