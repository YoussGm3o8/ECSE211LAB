import subsystem.car as car
import time
from common.constants_params import *
from common.filters import Diff



TURN_SPEED = 150
FORWARD_SPEED = 150
TIMER = 150

car = car.Car(debug=False)

def avoid_water(car):
    water_f = car.is_water()
    if water_f[0] == True:
        car.turn_right(TURN_SPEED)
        while water_f[0] == True:
            car.update(0.05)
            water_f = car.is_water()
        time.sleep(0.2)
        car.forward(FORWARD_SPEED)
    if water_f[1] == True:
        car.turn_left(TURN_SPEED)
        while water_f[1] == True:
            car.update(0.05)
            water_f = car.is_water()
        time.sleep(0.2) #important to overturn
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


def scan(car, duration=10, treshold=25):
    if True: #car.clock % 30 == 0:
        print("---------------scanning ---------------")

        car.turn_left(TURN_SPEED)
        for i in range(duration):
            check_cube(car)
            avoid_water(car)

        car.turn_right(TURN_SPEED)
        for i in range(duration*2):
            check_cube(car)
            avoid_water(car)

        car.turn_left(TURN_SPEED)
        for i in range(duration):
            check_cube(car)
            avoid_water(car)

        car.forward(FORWARD_SPEED)
        time.sleep(0.1)
        car.stop()
    else:
        check_cube(car)

def check_wall(car):
    car.stop()
    avoiding = car.avoid_wall(15)
    if avoiding[0]:
        print("wall detected", avoiding[1])

        # car.reverse(TURN_SPEED, 2)
        car.wait_for_action()

        if avoiding[1] == "front":
            car.reverse(TURN_SPEED, 8)
            car.wait_for_action()
            car.turn_right(TURN_SPEED, 40)
            car.wait_for_action()
        elif avoiding[1] == "right":
            print("turn left for right wall")
            car.turn_left(TURN_SPEED, 20)
            car.wait_for_action()
        else:
            print("turn right for left wall")
            car.turn_right(TURN_SPEED, 20)
            car.wait_for_action()

        scan(car)

        car.forward(FORWARD_SPEED)
        
    else:
        scan(car)

def return_home(car):
    """
    assume you are at a border facing the wall
    """
    car.forward(FORWARD_SPEED)
    while True:
        car.update(0.05)
        if car.avoid_wall(15):
            break
        avoid_water(car)

    car.turn_left(TURN_SPEED)
    while(car.state.right_color_sensor[-1] != 'o' or car.state.right_color_sensor[-1] != 'y' or car.state.right_color_sensor[-1] != 'r'):
        print(car.state.right_color_sensor) #this may be white
        car.update(0.05)

    car.turn_right(TURN_SPEED)
    while(car.state.right_color_sensor[-1] == 'y' or car.state.right_color_sensor[-1] == 'o' or car.state.right_color_sensor[-1] == 'r'):
        car.update(0.05)

    while True:
        car.update(0.05)
        if car.state.right_color_sensor[-1] == 'y' or car.state.right_color_sensor[-1] == 'o' or car.state.right_color_sensor[-1] == 'r':
            time.sleep(0.1) #adjust to overshoot
            car.wheel_left(TURN_SPEED) #if this makes no sense its because the ports are wrong so ignore
            car.wheel_right(150)
        else:
            car.wheel_left(150)
            car.wheel_right(TURN_SPEED)


try:
    ti = time.time()
    car.forward(FORWARD_SPEED)
    while True:
        if time.time() - ti > TIMER:
            print("time to return home!")
            break
        print("flag: ", car.flag)
        car.update(0.025)
        check_wall(car)
        avoid_water(car)
        scan(car)

    while car.avoid_wall(100)[1] != "front":
        car.update()
        time.sleep(0.05)
        print("not front")
        if car.avoid_wall(100)[1] == "right":
            print("right")
            car.turn_right(100, 10)
            car.wait_for_action()
            car.forward(100)
            time.sleep(0.5)
            car.stop() 
        if car.avoid_wall(100)[1] == "left":
            print("left")
            car.turn_left(100, 10)
            car.wait_for_action()
            car.forward(100)
            time.sleep(0.5)
            car.stop() 
    return_home(car)
    car.dump_cubes()
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

