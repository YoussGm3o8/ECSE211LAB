import components.engine as engine
from components.engine import global_enable
from main import Poop_Scooper
from components.gyrosensor import GYRO_Sensor
from components.ultrasonic import US_Sensor
from components.colorsensor import Color_Sensor, Color_Sensor2
from common.constants_params import *
from common.constants_params import LEFT_WHEEL_PORT, RIGHT_WHEEL_PORT
from utils.brick import Motor, wait_ready_sensors, reset_brick
from subsystem.car import Car
import time

car = Car(GYRO_Sensor(GYRO_PORT), US_Sensor(US_PORT), Color_Sensor(COLOR_SENSOR), Color_Sensor2(COLOR_SENSOR_STICKER), Motor(LEFT_WHEEL_PORT), Motor(RIGHT_WHEEL_PORT), True)
wait_ready_sensors()
global_enable[1], global_enable[2] = False, False
car.debug = False
engine.start()

try:
    while True:
        state = engine.global_state.get()
        print("x: " , state.x_pos * 100, "y: " , state.y_pos * 100, "direction :", state.g_sensor % 360)
        
        car.forward_until_distance(360, 20)
        car.turn_car(180, 90)


finally:
    car.stop()
    reset_brick()
    engine.end()