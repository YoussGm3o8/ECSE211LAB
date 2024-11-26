import time
from common.constants_params import *

class Poop_Actions():
    def __init__(self, arm, dumb, us_sensor,
            color_sensor, color_sensor_sticker,
            debug):
        self.arm = arm
        self.dumb =dumb
        self.us_sensor = us_sensor
        self.color_sensor = color_sensor
        self.color_sensor_sticker = color_sensor_sticker
        self.debug = debug
        self.offset_arm_angle = self.arm.get_encoder()
        self.offset_dumb_angle = self.dumb.get_encoder()

    def is_poop(self):
        color = self.color_sensor.fetch()
        color_sticker = self.color_sensor_sticker.fetch()
        if self.debug:
                print(f"color {color} stciker_color {color_sticker}")
        return color == 'o' or color == 'y' or color_sticker == 'o' or color_sticker == 'y'
    
    def poop_checker(self):
        self.set_arm_to_angle(105, MODERATE)
        distance = self.us_sensor.fetch()
        if ( PICKUP_DISTANCE_LOWER <= distance and PICKUP_DISTANCE_UPPER >= distance):
            start_time = time.time()
            while time.time() - start_time < POOP_CHECK_TIME:
                if self.is_poop():
                    self.dumb.set_dps(-FASTER)
                    self.set_arm_to_angle(320, FASTER)
                    break
                time.sleep(0.5)
        self.dumb.set_dps(0)
        self.set_arm_to_angle(0, FAST)

    def set_arm_to_angle(self, target_angle, dps):
        self.set_motor_to_angle(-target_angle, dps, self.arm, self.offset_arm_angle)

    def set_dumb_to_angle(self, target_angle, dps):
        self.set_motor_to_angle(target_angle, dps, self.dumb, self.offset_dumb_angle)

    def set_motor_to_angle(self, target_angle, dps, motor, offset):
        init_angle = motor.get_encoder() - offset
        direction = target_angle - init_angle
        motor.set_dps(-dps if direction < 0 else dps)
        while True:
            current_position = motor.get_encoder() - self.offset_dumb_angle
            if self.debug:
                print(f"curr {current_position} target:{target_angle} init {init_angle} direction {direction} dps {dps}")
            if (direction > 0 and current_position >= target_angle):
                break
            if (direction < 0 and current_position <= target_angle):
                break
            time.sleep(0.05)
        motor.set_dps(0)

    def taking_meaurements(self): # for debugging please ignore
        while True:
            time.sleep(0.05)
            print(f"US: {self.us_sensor.fetch()} arm:{self.arm.get_encoder() - self.offset_arm_angle} color {self.color_sensor_sticker.fetch()} color_sticker: {self.color_sensor_sticker.fetch()}")
