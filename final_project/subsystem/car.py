import time
from components.ultrasonic import US_Sensor
from components.colorsensor import Color_Sensor, Color_Sensor2
from utils.brick import Motor, reset_brick
from common.constants_params import *
from collections import deque

class Car():
    """
    left wheel 186
    right wheel 180
    """
    def __init__(self, debug=True):

        self.us_sensor = US_Sensor(US_PORT)
        self.us_sensor_2 = US_Sensor(US_PORT_2)
        self.wheel_left = Motor(LEFT_WHEEL_PORT)
        self.wheel_right = Motor(RIGHT_WHEEL_PORT)
        self.left_color_sensor = Color_Sensor(COLOR_SENSOR)
        self.right_color_sensor = Color_Sensor2(COLOR_SENSOR_STICKER)

        self.debug = debug
        self.abs_angle_time = 0

        self.current_action = (None, None)
        self.target_distance = None
        self.target_time = None
        self.correction = 0
        self.is_stopped = True
        self.fix_memory = None

        self.clock = 0
        self.us_regions = deque(maxlen=3)

    def kill(self):
        reset_brick()

    def stop(self):
        if self.debug:
            print("Stopping")
        self.is_stopped = True
        self.wheel_left.set_dps(0)
        self.wheel_right.set_dps(0)

    def forward(self, dps, distance=None):

        if self.debug:
            print("Moving forward")
        self.is_stopped = False
        self.wheel_left.set_dps(dps)
        self.wheel_right.set_dps(dps)

        if distance is not None:
            self.wheel_left.reset_encoder()
            self.wheel_right.reset_encoder()
            self.target_distance = distance
        else:
            self.target_distance = None

        self.current_action = ("forward", dps)

    def reverse(self, dps, distance=None):
        if self.debug:
            print("Moving backward")
        if distance is not None:
            self.forward(-dps, -distance)
        else:
            self.forward(-dps)

    def distance_to_encoder_units(self, distance):
        ENCODER_TICKS_PER_REV = 360
        WHEEL_DIAMETER = 4.32
        wheel_circumference = WHEEL_DIAMETER * 3.14159  # Circumference = π * Diameter
        encoder_units_per_revolution = ENCODER_TICKS_PER_REV
        distance_per_encoder_unit = wheel_circumference / encoder_units_per_revolution

        # Convert distance to encoder units
        return int(distance / distance_per_encoder_unit)
    
    def encoder_units_to_distance(self, encoder_units):
        ENCODER_TICKS_PER_REV = 360
        WHEEL_DIAMETER = 4.32
        wheel_circumference = WHEEL_DIAMETER * 3.14159  # Circumference = π * Diameter
        encoder_units_per_revolution = ENCODER_TICKS_PER_REV
        distance_per_encoder_unit = wheel_circumference / encoder_units_per_revolution

        # Convert encoder units to distance
        return encoder_units * distance_per_encoder_unit

    def turn(self, dps, time=None, auto_convert=True):
        """
        positive dps is left turn

        if auto_convert is true: time is defined in 20hz (1 count per 50ms)
        example: 20 is 1 second

        """
        if self.debug:
            print("Turning")
        self.is_stopped = False
        self.wheel_left.set_dps(dps)
        self.wheel_right.set_dps(-dps)

        if time is not None:
            if auto_convert:
                time = time * dps

            self.target_time = self.abs_angle_time + time
        else:
            self.target_time = None

        self.current_action = ("turn", dps)

    def turn_left(self, dps, time=None, auto_convert=True):
        self.turn(abs(dps), time, auto_convert)

    def turn_right(self, dps, time=None, auto_convert=True):
        self.turn(-abs(dps), time, auto_convert)

    def fix_angle(self, angle_time):
        """call this function to fix the angle of the car with the target angle"""
        if self.debug:
            print("Fixing angle, abs_angle_time: ", self.abs_angle_time, "angle_time: ", self.target_time)
        if self.clock % 2 == 0:
            self.fix_memory = (self.current_action, self.get_distance_remaining())
            if self.abs_angle_time > angle_time:
                self.turn_right(self.wheel_left.get_speed())
            elif self.abs_angle_time < angle_time:
                self.turn_left(self.wheel_left.get_speed())            
        else:
            if self.fix_memory is not None:
                if self.fix_memory[0][0] == "forward":
                    self.forward(self.fix_memory[0][1], self.fix_memory[1])
                else:
                    self.turn(self.fix_memory[0][1])

    def get_distance_remaining(self):
        if self.target_distance is not None:
            left_distance = -self.encoder_units_to_distance(self.wheel_left.get_encoder())
            right_distance = -self.encoder_units_to_distance(self.wheel_right.get_encoder())
            average_distance = (left_distance + right_distance) / 2
            if self.debug:
                print(f"Distance remaining: {self.target_distance - average_distance}")
            return self.target_distance - average_distance
        else:
            if self.debug:
                print("No target distance")
            return None

    def update(self):
        self.clock += 1
        if self.current_action[0] == "forward":
            if self.target_distance is not None:
                left_distance = self.encoder_units_to_distance(self.wheel_left.get_encoder())
                right_distance = self.encoder_units_to_distance(self.wheel_right.get_encoder())
                if (left_distance > right_distance):
                    self.correction = 10
                    print("left biased")
                elif (left_distance < right_distance):
                    self.correction = -10
                    print("right biased")
                else:
                    self.correction = 0
                average_distance = (left_distance + right_distance) / 2
                if self.current_action[1] is None:
                    self.stop()
                else:
                    if self.current_action[1] > 0:
                        if average_distance > self.target_distance:
                            self.stop()
                    elif self.current_action[1] < 0:
                        if average_distance < self.target_distance:
                            self.stop()
                    else:
                        self.stop()

        if self.current_action[0] == "turn":
            if self.current_action[1] is not None:
                self.abs_angle_time += self.current_action[1]
            if self.target_time is not None:
                print(self.target_time, self.abs_angle_time)
                if (self.target_time - self.abs_angle_time) * self.current_action[1] >= 0:
                    self.stop()

    def is_water(self):
        """
        returns a tuple (bool, bool) if color sensor detects blue or purple
        """
        c1 = self.left_color_sensor.fetch()
        c2 = self.right_color_sensor.fetch()
        c1_f = False
        c2_f = False

        if c1 == "b" or c1 == "p":
            c1_f = True
        if c2 == "b" or c2 == "p":
            c2_f = True
        
        return c1_f, c2_f

    def wait_for_action(self):
        while not self.is_stopped:
            time.sleep(0.05)
            self.update()

    def previous_action(self, **kargs):
        if self.current_action[0] == "forward":
            if kargs.get("target_distance") is None:
                self.forward(self.current_action[1], self.get_distance_remaining())
            else:
                self.forward(self.current_action[1], kargs["target_distance"])
        elif self.current_action[0] == "turn":
            if kargs.get("target_time") is None:
                if self.target_time is not None:
                    self.turn(self.current_action[1], self.target_time - self.abs_angle_time)
                else:
                    self.turn(self.current_action[1])
            else:
                self.turn(self.current_action[1], kargs["target_time"]) 

    def avoid_water(self, max_correction=40):

        flags = self.is_water()

        if self.debug:
            print("Water flags: ", flags)

        if flags[0] and flags[1]:
            td = self.get_distance_remaining()
            if self.target_time is not None:
                tt = self.target_time - self.abs_angle_time
            else:
                tt = None
            self.reverse(MODERATE, 5)
            self.wait_for_action()
            self.turn_left(MODERATE, 10)
            self.wait_for_action()
            self.previous_action(target_distance=td, target_time=tt)

        
        elif flags[0]:
            td = self.get_distance_remaining()
            speed = self.wheel_left.get_speed()
            if self.target_time is not None:
                tt = self.target_time - self.abs_angle_time
            else:
                tt = None
            self.turn_right(speed, max_correction)
            while True:
                time.sleep(0.05)
                self.update()
                if not self.is_water()[0] or self.is_stopped:
                    break
            self.previous_action(target_distance=td, target_time=tt)
        elif flags[1]:
            speed = self.wheel_left.get_speed()
            if self.target_time is not None:
                tt = self.target_time - self.abs_angle_time
            else:
                tt = None
            td = self.get_distance_remaining()
            self.turn_left(speed, max_correction)
            while True:
                time.sleep(0.05)
                self.update()
                if not self.is_water()[1] or self.is_stopped:
                    break
            self.previous_action(target_distance=td, target_time=tt)

    def detect_objects(self, treshold=15, desync=False):
        if not desync:
            us1 = self.us_sensor.fetch()
            us2 = self.us_sensor_2.fetch()
        elif self.clock % 2 == 0:
            us1 = self.us_sensor.fetch()
            us2 = treshold #skip the sensor
        else:
            us1 = treshold #skip the sensor
            us2 = self.us_sensor_2.fetch()

        if us1 < treshold or us2 < treshold:
            return us1, us2
        return None

    def which(self,tup, treshold=8):
        s1_f = False
        s2_f = False
        if tup[0] < treshold:
            s1_f = True
        if tup[1] < treshold:
            s2_f = True
        return s1_f, s2_f
    
    def get_us_tuple(self):
        val = self.us_sensor.fetch()
        val2 = self.us_sensor_2.fetch()
        if val is None or val2 is None:
            return None
        return val, val2
    
    def get_us_regions_prob(self):
        if len(self.us_regions) == 0:
            return None
        left = 0
        right = 0
        both = 0
        none = 0
        for i in self.us_regions:
            if i == "left":
                left += 1
            elif i == "right":
                right += 1
            elif i == "both":
                both += 1
            else:
                none += 1
        return left/len(self.us_regions), right/len(self.us_regions), both/len(self.us_regions), none/len(self.us_regions)


    def close_to_object_adjustment(self, treshold=5):
        tup = self.get_us_tuple()
        if tup is not None:
            pass

    def mini_scan(self, direction="left", treshold=4):
        if direction == "left":
            self.turn_left(50, 10)
        else:
            self.turn_right(50, 10)

        while not self.is_stopped:
            time.sleep(0.05)
            self.update()
            tup = self.get_us_tuple()
            if tup is not None:
                if min(tup) < treshold:
                    self.stop()
                    if tup.index(min(tup)) == 0:
                        print("object aligned with left sensor")
                        return "left"
                    else:
                        print("object aligned with right sensor")
                        return "right"

        print("no object detected, reverting back")
        if direction == "left":
            self.turn_right(50, 10)
            self.wait_for_action()
        else:
            self.turn_left(50, 10)
            self.wait_for_action()
        return None

    def scan(self, treshold=8, treshold2=4):
        tup = self.get_us_tuple()
        if tup is not None:
            mask = self.which(tup, treshold)
            if mask[0] and mask[1]:
                self.us_regions.append("both")
            elif mask[0]:
                self.us_regions.append("left")
            elif mask[1]:
                self.us_regions.append("right")
            else:
                self.us_regions.append("none")

        prob = self.get_us_regions_prob()
        if prob is not None:
            max_prob = max_prob.index(max(prob)) #argmax
            if max_prob == 3:
                return None

            dist = min(min(tup)*0.6, 4)
            self.forward(50, dist)
            while not self.is_stopped:
                self.update()
                time.sleep(0.05)
                tup = self.get_us_tuple()
                if tup is not None:
                    if min(tup) < treshold2:
                        self.stop()
                        if tup.index(min(tup)) == 0:
                            print("object aligned with left sensor")
                            return "left"
                        else:
                            print("object aligned with right sensor")
                            return "right"

            if max_prob == 0:
                print("object lost in left side")
                return self.mini_scan("left", treshold2)
            elif max_prob == 1:
                print("object lost in right side")
                return self.mini_scan("right", treshold2)
            else:
                print("object lost in middle")
                return self.mini_scan("left", treshold2)

        print("wall ahead or no object detected")
        return None

            



