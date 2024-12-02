import subsystem.car as car
import time
from common.constants_params import *
from common.filters import Diff



TURN_SPEED = 100
FORWARD_SPEED = 100
TIMER = 150

car = car.Car(debug=True)

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
    if car.avoid_wall(10):
        return
    object= car.mini_scan()
    if object is not None:
        car.stop()
        print(object)
        input("press any to continue")
        car.forward(FORWARD_SPEED)

def scan(car, duration=10, treshold=25):
    scanner = Diff(5, 1.5, 0.8)
    if car.clock % 100 == 0:
        print("---------------scanning ---------------")

        car.turn_left(TURN_SPEED)
        for i in range(duration):
            car.update(0.05)
            mini = car.mini_scan()
            if (scanner.update(time.time(), car.state.us_sensor if car.state.us_sensor < treshold else treshold)) or (mini is not None and mini != "us"):
                print("object found")
                car.stop()
                input("any input to continue")
                car.forward(FORWARD_SPEED)
            avoid_water(car)

        car.turn_right(TURN_SPEED)
        for i in range(duration*2):
            car.update(0.05)
            mini = car.mini_scan()
            if (scanner.update(time.time(), car.state.us_sensor if car.state.us_sensor < treshold else treshold)) or (mini is not None and mini != "us"):
                print("object found")
                car.stop()
                input("any input to continue")
                car.forward(FORWARD_SPEED)
            avoid_water(car)

        car.turn_left(TURN_SPEED)
        for i in range(duration):
            car.update(0.05)
            mini = car.mini_scan()
            if (scanner.update(time.time(), car.state.us_sensor if car.state.us_sensor < treshold else treshold)) or (mini is not None and mini != "us"):
                print("object found")
                car.stop()
                input("any input to continue")
                car.forward(FORWARD_SPEED)
            avoid_water(car)

        car.forward(FORWARD_SPEED)
    else:
        check_cube(car)

def check_wall(car):
    if car.avoid_wall(10):
        print("wall detected")

        car.reverse(TURN_SPEED, 10)
        car.wait_for_action()

        car.turn_left(TURN_SPEED)
        for _ in range(50):
            car.update(0.05)
            check_cube(car)
            avoid_water(car)

        car.forward(FORWARD_SPEED, 10)
        for _ in range(30):
            scan(car)
            car.update(0.05)
            # if car.avoid_wall(8):
            #     break
            avoid_water(car)

        car.turn_left(TURN_SPEED, 50)
        for _ in range(50):
            car.update(0.05)
            check_cube(car)
            avoid_water(car)

        car.forward(FORWARD_SPEED)

def return_home(car):
    """
    assume you are at a border facing the wall
    """
    car.turn_left(TURN_SPEED)
    while(car.state.right_color_sensor[-1] != 'r'):
        print(car.state.right_color_sensor) #this may be white
        car.update(0.05)

    car.turn_right(TURN_SPEED)
    while(car.state.right_color_sensor[-1] == 'r'):
        car.update(0.05)

    while True:
        car.update(0.05)
        if car.state.right_color_sensor[-1] == 'r':
            time.sleep(0.1) #adjust to overshoot
            car.wheel_left(TURN_SPEED) #if this makes no sense its because the ports are wrong so ignore
            car.wheel_right(150)
        else:
            car.wheel_left(150)
            car.wheel_right(TURN_SPEED)



def snake(car, speed, count,direction, odd=10):
    if count % odd == 0:
        if direction == 1:
            car.wheel_left.set_dps(speed)
            car.wheel_right.set_dps(speed*2)
        else:
            car.wheel_left.set_dps(speed*2)
            car.wheel_right.set_dps(speed)
        return -direction
    else:
        return direction

#make sure to extend the color sensors
try:
    ti = time.time()
    snake_direction = 1
    count = 0
    snake(car, 100, count, snake_direction)
    while True:
        if time.time() - ti > TIMER:
            print("time to return home!")
        print(car.flag)
        car.update(0.05)
        check_wall(car)
        avoid_water(car)
        direction = snake(car, FORWARD_SPEED, count, snake_direction)
        count += 1
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

