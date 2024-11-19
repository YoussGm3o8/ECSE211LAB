from components import navigation, gyrosensor
from utils.brick import wait_ready_sensors, reset_brick
import time

DEGREE = 1485 * 3
CALIBRATION_GYRO =  0.999

def calibrate_gyro():
    navigation.set_limits(180)
    navigation.wheel_right.set_position_relative(-DEGREE)
    navigation.wheel_left.set_position_relative(DEGREE)
wait_ready_sensors(True)
calibrate_gyro()
si = time.time()
try:
    while True:
        print(gyrosensor.g_sensor.fetch() * CALIBRATION_GYRO)
        if -1 < navigation.wheel_left.get_speed() < 1:
            if time.time() - si > 3:
                break
finally:
    reset_brick()

