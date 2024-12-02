import time
from components.ultrasonic import US_Sensor
from components.colorsensor import Color_Sensor, Color_Sensor2
from utils.brick import Motor, reset_brick
from common.constants_params import *
from collections import deque, namedtuple
from common.filters import Median_Filter
from enum import Enum

state= namedtuple("state", ["us_sensor", "us_sensor_2", "left_color_sensor", "right_color_sensor", "arm", "dump"])

class Flags(Enum):
    """
    in case unexpected behavior occurs flag is storred in car.flag
    """
    NONE = 0
    ERROR = 1
    WATER = 2
    WALL = 3
    FORWARD_COMPLETE = 4
    TURN_COMPLETE = 5
    OBJECT = 6

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
        self.arm = Motor(ARM_PORT)
        self.dump = Motor(DUMB_PORT)

        self.debug = debug
        self.abs_angle_time = 0

        self.current_action = (None, None)
        self.target_distance = None
        self.target_time = None

        self.is_stopped = True
        self.flag = Flags.NONE

        self.fix_memory = None
        self.state = state(None, None, None, None, None, None)

        self.clock = 0
        self.color_vote = deque(maxlen=5)
        self.color_vote_2 = deque(maxlen=5)

        self.median_filter = Median_Filter(5)
        self.median_filter_2 = Median_Filter(5)
    
    def dump_cubes(self):
        self.arm.set_position_relative(120)
        time.sleep(0.3)
        self.dump.reset_position()
        self.dump.set_limits(0, 220)
        self.dump.set_position_relative(120)
        time.sleep(1)
        self.dump.set_position_relative(-120)
        time.sleep(0.3)
        self.arm.set_position_relative(-120)

    def arm_reset(self):
        self.arm.set_limits(0, 220)
        self.arm.set_dps(-1)
        time.sleep(0.1)
        self.arm.set_dps(0)
        self.arm.reset_position()

    def arm_down(self):
        self.arm.set_limits(0, 220)
        self.arm.reset_position()
        self.arm.set_position_relative(320)
        time.sleep(2)
    
    def arm_up(self):
        self.arm.set_limits(0, 220)
        self.arm.set_position_relative(-420)
        time.sleep(2)
        self.arm_reset()

    def collect_cube(self):
        self.arm_reset()
        self.reverse(100)
        time.sleep(1.2)
        self.arm_down()
        self.forward(150)
        time.sleep(2.5)
        self.stop()
        self.arm_up()


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

    def update(self, sleep=None, update_state=True, filter_colors=False):
        if self.debug:
            print(self.current_action)
        self.clock += 1
        if self.current_action[0] == "forward":
            if self.target_distance is not None:
                left_distance = self.encoder_units_to_distance(self.wheel_left.get_encoder())
                right_distance = self.encoder_units_to_distance(self.wheel_right.get_encoder())
                average_distance = (left_distance + right_distance) / 2

                if self.current_action[1] is None:
                    self.stop()
                    self.flag = Flags.ERROR
                else:
                    if self.current_action[1] > 0:
                        if average_distance > self.target_distance:
                            self.stop()
                            self.flag = Flags.FORWARD_COMPLETE
                    elif self.current_action[1] < 0:
                        if average_distance < self.target_distance:
                            self.stop()
                            self.flag = Flags.FORWARD_COMPLETE
                    else:
                        self.stop()
                        self.flag = Flags.ERROR
                    

        if self.current_action[0] == "turn":
            if self.current_action[1] is not None:
                self.abs_angle_time += self.current_action[1]
            if self.target_time is not None:
                print(self.target_time, self.abs_angle_time)
                if (self.target_time - self.abs_angle_time) * self.current_action[1] <= 0:
                    self.stop()
                    self.flag = Flags.TURN_COMPLETE

        if update_state:
            if filter_colors:
                self.color_vote.append(self.left_color_sensor.fetch())
                self.color_vote_2.append(self.right_color_sensor.fetch())
                self.state = state(self.us_sensor.fetch(), self.us_sensor_2.fetch(), self.get_color(self.color_vote), self.get_color(self.color_vote_2), None, None)
            else:
                self.state = state(self.us_sensor.fetch(), self.us_sensor_2.fetch(), self.left_color_sensor.fetch(), self.right_color_sensor.fetch(), None, None)

        if sleep is not None:
            time.sleep(sleep)

    def is_water(self):
        """
        returns a tuple (bool, bool) if color sensor detects blue or purple
        Waits until color sensors provide non-null values
        """
        while self.state.left_color_sensor is None or self.state.right_color_sensor is None:
            self.update(0.05)
        
        c1 = self.state.left_color_sensor
        c2 = self.state.right_color_sensor
        c1_f = False
        c2_f = False

        if c1 == "ub" or c1 == "up":
            c1_f = True
        if c2 == "ub" or c2 == "up":
            c2_f = True
        
        return c1_f, c2_f
    
    def wait_for_action(self, timeout=None):
        if timeout is not None:
            ti = time.time()
        while not self.is_stopped:
            self.update(0.05)
            if timeout is not None:
                if time.time() - ti > timeout:
                    break

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
        previous_flag = self.flag

        if self.debug:
            print("Water flags: ", flags)

        if flags[0] == False and flags[1] == False:
            return
        if flags[0] and flags[1]:
            self.flag = Flags.WATER
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
            self.flag = Flags.WATER
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
            self.flag = Flags.WATER
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

        self.flag = previous_flag

    def mini_scan(self, treshold=5):
        
        if self.state.left_color_sensor is not None and self.state.left_color_sensor[0] != "u":
            # self.stop()
            # self.flag = Flags.OBJECT
            return "left"
        if self.state.right_color_sensor is not None and self.state.right_color_sensor[0] != "u":
            # self.stop()
            # self.flag = Flags.OBJECT
            return "right"

        return None

    def avoid_wall(self, treshold=15) -> bool:
        if self.state.us_sensor_2 < treshold and self.state.us_sensor < treshold:
                self.flag = Flags.WALL
                self.stop()
                return True
        return False

    def reset_flag(self):
        self.flag = Flags.NONE

    def get_color(self, colors):
        return max(colors, key=colors.count)  

    def timer(self, modulo=200):
        if self.clock % modulo == 0:
            return True
        return False

    def scan_left(self, turning_time=20, treshold=20, upper_bound=60):
        return self.scan(1, turning_time, treshold, upper_bound)
    
    def scan_right(self, turning_time=20, treshold=20, upper_bound=60):
        return self.scan(-1, turning_time, treshold, upper_bound)

    def scan(self, direction=1, turning_time=20, treshold=20, upper_bound=60):
        no_filter = False
        self.turn(MODERATE * direction, time=turning_time)

        while self.is_stopped:
            self.update(sleep=0.05)
            
            # Wait for non-null sensor readings
            while (self.state.us_sensor is None or 
                self.state.us_sensor_2 is None):
                self.update(sleep=0.05)
            
            us1 = self.median_filter.update(self.state.us_sensor) if self.state.us_sensor < upper_bound else self.median_filter.update(upper_bound)
            us2 = self.median_filter_2.update(self.state.us_sensor_2) if self.state.us_sensor_2 < upper_bound else self.median_filter_2.update(upper_bound)
            
            if us2 < upper_bound and us1 < upper_bound and self.state.us_sensor_2 - self.state.us_sensor > treshold:
                no_filter = True
            if abs(us2 - us1) > treshold:
                return True, no_filter
        
        return False, no_filter
