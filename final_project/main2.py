import subsystem.car as car
import time
from common.constants_params import *
from common.filters import Diff




car = car.Car(debug=True)


def avoid_water(car):
    water_f = car.is_water()
    print(water_f)
    if water_f[0] == True:
        car.turn_right(100)
        while water_f[0] == True:
            car.update(0.05)
            water_f = car.is_water()
            print(water_f)
            print("water turning")
        time.sleep(0.1)
        print("forward")
        car.forward(150)
    if water_f[1] == True:
        car.turn_left(100)
        while water_f[1] == True:
            car.update(0.05)
            water_f = car.is_water()
            print(water_f)
            print("water turning")
        time.sleep(0.1)
        print("forward")
        car.forward(150)

def check_cube(car):
    if car.avoid_wall(8):
        return
    object= car.mini_scan()
    if object is not None:
        car.stop()
        print(object)
        input("press any to continue")
        car.forward(150)

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


def scan(car, duration=10, treshold=25):
    scanner = Diff(5, 2, 0.8)
    if car.clock % 100 == 0:
        print("scanning ---------------")
        car.turn_left(100)
        for i in range(duration):
            car.update(0.05)
            mini = car.mini_scan()
            if (scanner.update(time.time(), car.state.us_sensor if car.state.us_sensor < treshold else treshold)) or (mini is not None and mini != "us"):
                print("object found")
                car.stop()
                input("any input to continue")
                car.forward(150)
            avoid_water(car)
        car.turn_right(100)
        for i in range(duration*2):
            car.update(0.05)
            mini = car.mini_scan()
            if (scanner.update(time.time(), car.state.us_sensor if car.state.us_sensor < treshold else treshold)) or (mini is not None and mini != "us"):
                print("object found")
                car.stop()
                input("any input to continue")
                car.forward(150)
            avoid_water(car)
        car.turn_left(100)
        for i in range(duration):
            car.update(0.05)
            mini = car.mini_scan()
            if (scanner.update(time.time(), car.state.us_sensor if car.state.us_sensor < treshold else treshold)) or (mini is not None and mini != "us"):
                print("object found")
                car.stop()
                input("any input to continue")
                car.forward(150)
            avoid_water(car)
        car.forward(150)
    else:
        check_cube(car)


try:
    car.forward(150)
    while True:
        print(car.flag)
        car.update(0.05)
        if car.avoid_wall(10):
            print("wall detected")
            car.reverse(100, 10)
            car.wait_for_action()
            car.turn_left(100)
            for i in range(50):
                car.update(0.05)
                check_cube(car)
                avoid_water(car)
            car.forward(150, 10)
            for i in range(30):
                car.update(0.05)
                scan(car)
                avoid_water(car)
            car.turn_left(100, 50)
            for i in range(50):
                car.update(0.05)
                check_cube(car)
                avoid_water(car)
            car.forward(150)
        avoid_water(car)

        scan(car)
finally:
    car.kill()
