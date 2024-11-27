import time
from subsystem.poop_handle import Poop_Actions
from common.constants_params import *

class Traversal():
    def __init__(self, car, poop_picker, color_sensor, color_sensor_sticker, us_sensor, debug):
        self.car = car 
        self.poop_picker = poop_picker 
        self.color_sensor = color_sensor 
        self.color_sensor_sticker = color_sensor_sticker
        self.us_sensor = us_sensor,
        self.debug = debug

    def check_lane(self, direction):
        self.car.forward_until_distance(FAST, CHECK_WALL_DISTANCE)

        if self.is_wall():
            print("IT is a wall")
            self.car.turn_left(FASTER, 90 * direction)

    def is_wall(self):
        start_time = time.time()
        self.poop_picker.set_arm_to_angle(220, FASTER)
        time.sleep(1) # wait for arm to stabilize
        while time.time() - start_time < WALL_CHECK_TIME:
            if self.is_wall_color():
                self.poop_picker.set_arm_to_angle(0, FASTER)
                return True
        self.poop_picker.set_arm_to_angle(0, FASTER)
        return False
    
    def is_wall_color(self):
        color = self.color_sensor.fetch()
        color_sticker = self.color_sensor_sticker.fetch()
        print(f"color {color} sticker_color {color_sticker}")
        if self.debug:
                print(f"color {color} stciker_color {color_sticker}")
        return color == 'w' # or color_sticker == 'w'


#I don't know why we would need threading or if its advantageous to use it in this case
# def avoid_water_using_threads():
#     try:
#         start()
#         while True:
#             state = global_state.get()
#             if state.color_sensor == "b" or state.color_sensor == "p":
#                 nav.turn(SLOW)
#                 print("right")
#             elif state.color_sensor2 == "b" or state.color_sensor2 == "p":
#                 nav.turn(-SLOW)
#                 print("left")
#             else:
#                 nav.forward(MODERATE)
#                 print("forward")
#     finally:
#         end()