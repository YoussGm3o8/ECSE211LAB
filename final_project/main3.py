import subsystem.car as car
import time
from common.constants_params import *

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
    object= car.mini_scan()
    if object is not None:
        if object == "us":
            is_cube = scan(car)
            if is_cube:
                car.stop()
                print("cube detected")
                input("press any to continue")
                car.forward(150)
            else:
                wall(car)
        else:
            car.stop()
            print(object)
            input("press any to continue")
            car.forward(150)


def scan(car):
    car.turn_left(100)
    for i in range(30):
        car.update(0.05)
        avoid_water(car)
        car.mini_scan()
        if car.mini_scan() is not None and car.mini_scan() != "us":
            return True
    car.turn_right(100)
    for i in range(30):
        car.update(0.05)
        avoid_water(car)
        car.mini_scan()
        if car.mini_scan() is not None and car.mini_scan() != "us":
            return True
    return False

def scan_v2(car):
    car.turn_left(100)
    for _ in range(30):
        car.update(0.05)
        avoid_water(car)
        check_cube(car)
    car.turn_right(100)
    for _ in range(30):
        car.update(0.05)
        avoid_water(car)
        check_cube(car)

def wall(car):
    print("wall detected")
    car.reverse(100, 10)
    car.wait_for_action()
    car.turn_left(100)
    for i in range(50):
        car.update(0.05)
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


try:
    car.forward(150)
    count = 0
    while True:
        print(car.flag)
        car.update(0.05)
        check_cube(car)
        avoid_water(car)
        count += 1
        if count % 50 == 0:
            scan_v2(car)

finally:
    car.kill()