from common.filters import Diff, Median_Filter
import time
from communication.client import Client
from collections import namedtuple
from components.gyrosensor import GYRO_Sensor
from components.ultrasonic import US_Sensor
from common.constants_params import *
from subsystem.car import Car
from utils.brick import Motor, reset_brick

median = Median_Filter(5)

def scan_for_objects(car, degree, direction=1):
    assert(isinstance(car, Car))
    scan = Diff(5, 30, 0.7)
    # d = Diff(2.5, 20, 0.7) #ideally we change these parameters for each distances (close, medium, far)
    # d2 = Diff(5, 50, 1) #ideally we change these parameters for each distances (close, medium, far)
    car.wheel_left.set_dps(SLOW * direction)
    car.wheel_right.set_dps(-SLOW * direction)
    initial_angle = car.g_sensor.fetch()

    while True:
        current_angle = car.g_sensor.fetch()
        if abs(initial_angle - current_angle) > degree:
            car.stop()
            return False
        distance = median.update(car.us_sensor.fetch())
        if scan.update(current_angle, distance):
            car.wheel_left.set_dps(-SLOW * direction)
            car.wheel_right.set_dps(SLOW * direction)
            target_angle = scan.down[-1][0]
            while abs(target_angle - current_angle) > 5: #change this so that instead of abs distance we have the signed distance
                time.sleep(0.05)
                current_angle = car.g_sensor.fetch()
            car.stop()
            return True
        time.sleep(0.05)


def forward_listen(car, dps, distance_treshold, target_angle=None, client_callback=None):
    """
    Move forward until the distance jumps by 10 cm (an object has moved from the sensor).
    ADJUSTMENTS: The car keeps moving ifs that object was 40+ cm away from the sensor (in theory the car shouldn't hit it).
    """
    assert(isinstance(car, Car))
    median.clear()
    last_dist = median.update(Car.us_sensor.fetch())
    if target_angle is None:
        target_angle = car.g_sensor.fetch()
    while last_dist > 10:
        car.keep_angle_at(target_angle, [0, dps, dps], 1)
        current_dist = median.update(Car.us_sensor.fetch())
        diff = current_dist - last_dist
        if current_dist < distance_treshold and diff > 10:
            car.stop()
            return last_dist, target_angle
        last_dist = current_dist
        time.sleep(0.05)
        if client_callback is not None:
            client_callback(("forward_listen", (car.cur_angle, current_dist)))
    return None


def refocus(car, dps, target_distance, distance_treshold):
    """rotate the car very slightly to make adjustments with the disappearing object"""
    assert(isinstance(car, Car))
    car.turn_left(dps, 5)
    if  target_distance - distance_treshold < car.us_sensor.fetch() < target_distance + distance_treshold:
        return True
    car.turn_right(dps, 10)
    if  target_distance - distance_treshold < car.us_sensor.fetch() < target_distance + distance_treshold:
        return True
    car.turn_left(dps, 5)
    return False

if __name__ == "__main__":
    cl = Client()
    try:
        car = Car(GYRO_Sensor(GYRO_PORT), US_Sensor(US_PORT), None, None, Motor(LEFT_WHEEL_PORT), Motor(RIGHT_WHEEL_PORT), True)
        res = -1
        target_angle = None
        while True:
            res, target_angle = forward_listen(car, 180, 40, target_angle, cl.send)
            if res is None:
                break
            target = refocus(car, 140, res, 7)
            if target == True:
                target_angle = None #reset the target angle
        
    finally:
        car.stop()
        reset_brick()
