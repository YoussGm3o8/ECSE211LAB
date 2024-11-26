import time
from common.constants_params import *

class Car():
    def __init__(self, g_sensor, us_sensor,
            color_sensor, color_sensor_sticker,
            wheel_left, wheel_right, debug):
        self.g_sensor = g_sensor
        self.us_sensor = us_sensor
        self.wheel_left = wheel_left
        self.wheel_right = wheel_right
        self.color_sensor = color_sensor
        self.color_sensor_sticker = color_sensor_sticker
        self.debug = debug
        self.cur_angle = 0

    def turn_left(self, dps, angle):
        self.turn_car(dps, -angle)

    def turn_right(self, dps, angle):
        self.turn_car(dps, angle)

    def stop(self):
        self.wheel_left.set_dps(0)
        self.wheel_right.set_dps(0)

    def forward_until_distance(self, dps, target_distance):
        cur_distance = self.us_sensor.fetch()
        prev_distance = cur_distance
        distance_thresholds = self.get_distance_thresholds(dps)

        while cur_distance > target_distance :
            remaining_distance = cur_distance - target_distance
            if self.debug:
                print(f"cur dist {cur_distance} prev {prev_distance} tar dist {target_distance} rem dist {remaining_distance}")
            self.keep_angle_at(self.cur_angle, distance_thresholds, remaining_distance)

            prev_distance = cur_distance
            cur_distance = self.us_sensor.fetch()
            time.sleep(0.05)
        self.stop()
        time.sleep(SLEEP_TIME)
        final_distance = self.us_sensor.fetch()
        if final_distance < target_distance:
            self.reverse(dps, target_distance - final_distance)
        if self.debug:
            print(f"Final distance: {final_distance}")

    def forward(self, dps, target_distance):
        cur_distance = self.us_sensor.fetch()
        start_position = self.wheel_right.get_encoder()
        target_position = start_position - self.distance_to_encoder_units(target_distance)
        distance_thresholds = self.get_distance_thresholds(dps)
        remaining_distance = self.get_remaining_distance(target_position, target_distance)
        while remaining_distance > 0:
            if self.us_sensor.fetch() < EMERGENCY_STOP_DISTANCE and target_distance > 0:
                break
            self.keep_angle_at(self.cur_angle, distance_thresholds, remaining_distance)
            remaining_distance = self.get_remaining_distance(target_position, target_distance)
            time.sleep(0.05)
        self.stop()
        if self.debug:
            time.sleep(SLEEP_TIME)
            print(f"Distance traveled: {cur_distance - self.us_sensor.fetch()}")

    def reverse(self, dps, target_distance):
        self.forward(-dps, -target_distance)

    def turn_car(self, dps, angle):
        """
        dps : speed of the car
        angle: turn the car by the relative angle. Positive is right turn, negative is left
        """
        new_angle = self.cur_angle + angle
        read_angle = self.g_sensor.fetch()
        angle_thresholds = self.get_angle_thresholds(dps)
        
        while True:
            angle_diff = read_angle - new_angle
            if self.debug:
                print(f"diff {angle_diff}, cur {self.cur_angle}")
            if abs(angle_diff % 360) <= 0:
                break
            if angle_diff > 0 and abs(angle_diff % 360) > 0:
                for threshold, right_dps, left_dps in angle_thresholds:
                    if abs(angle_diff) > threshold:
                        self.wheel_left.set_dps(left_dps)
                        self.wheel_right.set_dps(right_dps)
                        break
            else:
                for threshold, left_dps, right_dps in angle_thresholds:
                    if abs(angle_diff) > threshold:
                        self.wheel_left.set_dps(left_dps)
                        self.wheel_right.set_dps(right_dps)
                        break
            read_angle = self.g_sensor.fetch()
            time.sleep(0.05)
        self.stop()
        self.cur_angle = new_angle
        if self.debug:
            time.sleep(SLEEP_TIME)
            print(f"Final angle: {self.g_sensor.fetch()}, turned {'right' if angle > 0 else 'left' if angle < 0 else 'not turned'}")

    def keep_angle_at(self, angle, distance_thresholds, remaining_distance): # might be used for making turns
        read_angle = self.g_sensor.fetch()
        angle_diff = read_angle - angle
        for threshold, left_dps, right_dps in distance_thresholds:
            if remaining_distance > threshold:
                self.wheel_left.set_dps(left_dps)
                self.wheel_right.set_dps(right_dps)
                break
        if angle_diff > 0:
            self.wheel_left.set_dps(left_dps + angle_diff * 10)
        elif angle_diff < 0:
            self.wheel_right.set_dps(right_dps - angle_diff * 10)

    def get_remaining_distance(self, target_position, target_distance):
        current_position =self.wheel_right.get_encoder()  # Fetch the current encoder position
        if target_distance >= 0 :
            remaining_distance = current_position - target_position
            remaining_distance = self.encoder_units_to_distance(remaining_distance)
        else:
            remaining_distance = target_position - current_position
            remaining_distance = self.encoder_units_to_distance(remaining_distance)
        if self.debug:
            print(f"remainig dist {abs(remaining_distance)}")
        return remaining_distance
        

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

    def get_angle_thresholds(self, dps):
        correction_dps = MODERATE
        return [
            (30, -dps, dps),
            (25, -correction_dps * 4 // 5, correction_dps * 4 // 5),
            (20, -correction_dps * 3 // 5, correction_dps * 3 // 5),
            (15, -correction_dps * 2 // 5, correction_dps * 2 // 5),
            (10, -correction_dps // 5, correction_dps // 5),
        ]
    
    def get_distance_thresholds(self, dps):
        correction_dps = dps // 2  # Moderate speed for fine control
        return [
            (15, -dps, -dps),                          # Full speed if distance > 50
            (0, -correction_dps * 4 // 5, -correction_dps * 4 // 5),  # 80% of correction speed
            # (15, -correction_dps * 3 // 5, -correction_dps * 3 // 5),  # 60% of correction speed
        ]

