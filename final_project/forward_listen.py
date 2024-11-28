from common.filters import Diff, Median_Filter
import time
from communication.client import Client
from collections import namedtuple
from components.gyrosensor import GYRO_Sensor
from components.ultrasonic import US_Sensor
from common.constants_params import *
from subsystem.car import Car_V2, Car
from utils.brick import Motor, reset_brick
from components.ultrasonic import US_Sensor

median = Median_Filter(1)

def scan_for_objects(car, degree, direction=1):
    assert(isinstance(car, Car_V2))
    scan = Diff(5, 30, 0.7)
    # d = Diff(2.5, 20, 0.7) #ideally we change these parameters for each distances (close, medium, far)
    # d2 = Diff(5, 50, 1) #ideally we change these parameters for each distances (close, medium, far)
    car.wheel_left.set_dps(MODERATE * direction)
    car.wheel_right.set_dps(-MODERATE * direction)
    initial_angle = car.g_sensor.fetch()

    while True:
        current_angle = car.g_sensor.fetch()
        if abs(initial_angle - current_angle) > degree:
            car.stop()
            return False
        distance = median.update(car.us_sensor.fetch())
        if scan.update(current_angle, distance):
            car.wheel_left.set_dps(-MODERATE * direction)
            car.wheel_right.set_dps(MODERATE * direction)
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
    assert(isinstance(car, Car_V2))
    print("forward_listen")
    median.clear()
    last_dist = median.update(car.us_sensor.fetch())
    if target_angle is None:
        target_angle = car.g_sensor.fetch()
    while last_dist > 10:
        car.keep_angle(target_angle, dps, dps)
        current_dist = median.update(car.us_sensor.fetch())
        diff = current_dist - last_dist
        print("diff", diff, "dist", current_dist)
        if current_dist < distance_treshold and diff > 5:
            car.stop()
            return last_dist, target_angle
        last_dist = current_dist
        time.sleep(0.05)
        if client_callback is not None:
            client_callback(("forward_listen", (car.cur_angle, current_dist)))
    return None, None


def refocus(car, dps, target_distance, distance_treshold):
    """rotate the car very slightly to make adjustments with the disappearing object"""
    assert(isinstance(car, Car_V2))
    car.wheel_left.set_dps(-dps)
    car.wheel_right.set_dps(dps)
    for i in range(10):
        time.sleep(0.05)
        if  target_distance - distance_treshold < car.us_sensor.fetch() < target_distance + distance_treshold:
            return True
    
    car.wheel_left.set_dps(dps)
    car.wheel_right.set_dps(-dps)
    for i in range(20):
        time.sleep(0.05)
        if  target_distance - distance_treshold < car.us_sensor.fetch() < target_distance + distance_treshold:
            return True
    car.stop()
    return False


def quick_scan(car=Car_V2(GYRO_Sensor(GYRO_PORT), US_Sensor(US_PORT), None, None, Motor(LEFT_WHEEL_PORT), Motor(RIGHT_WHEEL_PORT), False)
, dps=MODERATE):
    last_dist = median.update(car.us_sensor.fetch())
    car.wheel_left.set_dps(dps)
    car.wheel_right.set_dps(-dps)
    for i in range(15):
        print(last_dist)
        if last_dist < 15:
            car.stop()
            return True
        last_dist = median.update(car.us_sensor.fetch())
        time.sleep(0.05)

    car.wheel_left.set_dps(-dps)
    car.wheel_right.set_dps(dps)
    for i in range(30):
        print(last_dist)
        if last_dist < 15:
            car.stop()
            return True
        last_dist = median.update(car.us_sensor.fetch())
        time.sleep(0.05)
    car.wheel_left.set_dps(dps)
    car.wheel_right.set_dps(-dps)
    for i in range(15):
        print(last_dist)
        if last_dist < 15:
            car.stop()
            return True
        last_dist = median.update(car.us_sensor.fetch())
        time.sleep(0.05)
    car.stop()
    return False

if __name__ == "__main__":
    try:
        # cl = Client()
        s1 = US_Sensor(US_PORT)
        s2 = US_Sensor(GYRO_PORT)
        for i in range(1000):
            print(s1.fetch(), s2.fetch())

            time.sleep(0.05)
            # cl.send(("forward_listen", (time.time(), val)))
                
    finally:
        reset_brick()
