import time

from common.wrappers import Filtered_Sensor
from common.filters import Median_Filter

from components.gyrosensor import GYRO_Sensor
from components.ultrasonic import US_Sensor
from components.colorsensor import Color_Sensor, Color_Sensor2
from subsystem.car import Car
from subsystem.poop_handle import Poop_Actions
from subsystem.traversal import Traversal
from common.constants_params import *
from utils.brick import Motor, wait_ready_sensors

class Poop_Scooper():

    def __init__(self):
        self.arm = Motor(ARM_PORT)
        self.dumb = Motor(DUMB_PORT)
        self.g_sensor = GYRO_Sensor(GYRO_PORT)
        self.us_sensor = Filtered_Sensor(US_Sensor(US_PORT), Median_Filter(5))
        self.wheel_left = Motor(LEFT_WHEEL_PORT)
        self.wheel_right = Motor(RIGHT_WHEEL_PORT)
        self.color_sensor = Color_Sensor(COLOR_SENSOR)
        self.color_sensor_sticker = Color_Sensor2(COLOR_SENSOR_STICKER)
        self.debug = True
        self.init_all_connected()

        self.my_car = Car(
            self.g_sensor, self.us_sensor,
            self.color_sensor, self.color_sensor_sticker,
            self.wheel_left, self.wheel_right, self.debug
            )
        self.my_poop_picker = Poop_Actions(
            self.arm,
            self.dumb,
            self.us_sensor,
            self.color_sensor,
            self.color_sensor_sticker,
            self.debug
        )
        self.traversal = Traversal(
            self.my_car,
            self.my_poop_picker,
            self.color_sensor,
            self.color_sensor_sticker,
            self.us_sensor,
            self.debug
        )



        time.sleep(INITILIALIZATION_TIME) # for car to initilaize all sensors

    def init_all_connected(self):
        start_time = time.time()
        while time.time() - start_time < INIT_GRIPPER_TIME:
            self.arm.set_dps(VERY_SLOW)
        self.arm.set_dps(0)
        self.dumb.set_dps(0)
        self.arm.reset_position()
        self.dumb.reset_position()
        self.g_sensor.reset()
        self.color_sensor.fetch()
        self.color_sensor_sticker.fetch()
        while self.us_sensor.fetch == 0:
            if self.debug:
                print ("Waiting for us sensor")
    

    def do_something(self): # for developemt
        # self.my_poop_picker.set_dumb_to_angle( 107, FAST)
        # time.sleep(1.5)
        # self.my_poop_picker.set_dumb_to_angle( 2, VERY_FAST)
        # time.sleep(1)
        direction = 1
        for i in range(6):
            direction = direction * -1
            self.traversal.check_lane(direction)
            self.my_car.forward(FAST, 20)
            self.my_car.turn_left(FAST, 90 * direction)
    
    def taking_meaurements(self): # for debugging please ignore
        while True:
            time.sleep(0.05)
            print(f"US: {self.us_sensor.fetch()} color_sticker: {self.color_sensor_sticker.fetch()}")


if __name__ == "__main__":
    poop = Poop_Scooper()
    # poop.do_something()
    # poop.taking_meaurements()



