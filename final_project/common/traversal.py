from collections import deque
import time
"""
Global state for devices (used to interact between threads)

usage:
global_state = {us_sensor, color_sensor1, color_sensor2, g_sensor, ...}
PLEASE DEFINE ADDTIONAL SENSORS IF NEEDED (ADD TO THE LIST ABOVE AT '...')
color = p, o, y, g, r, b, UNKNOWN, NONE
-assuming we have go to position while avoiding obstacles and water
-map_len = 122

void go_to_position (int final_position): A function that goes to final_position that goes in a
straight line, while avoiding water, obstacles and collecting poop. 
"""
map_len = 122
#global_state have been moved to components.engine


class Traversal:
    """
blue_cube    
    """
    def __init__(self):
        self.cur_position = (0, 0)
        self.starting_point = position
        self.buffer = []
        grid_width = map_len/8

    def traverse_row(self):
        cur_x, cur_y = cur_position
        go_to_position(cur_position, (map_len, cur_y))

    def go_to_next_row(self, direction):
        cur_x, cur_y = cur_position
        go_to_position(cur_position, (cur_x, cur_y + grid_width))

    def go_back_home(self):
        go_to_position(cur_position, starting_point)

    def go_to_position(self, final_position):
        scan_interval = 10
        cubes_position = scan(scan_interval)


