import math
import time
# from components.gyrosensor import g_sensor
from components.ultrasonic import us_sensor
from components.colorsensor import color_sensor, color_sensor2
from common.constants_params import LEFT_WHEEL_PORT, RIGHT_WHEEL_PORT
from main import Poop_Scooper as nav
from common.wrappers import Filtered_Sensor
from common.filters import Median_Filter
from common import threads
from queue import Queue
from collections import namedtuple
from utils.brick import reset_brick

# IMPORTANT: Replace these with your robot's actual measurements
WHEEL_DIAMETER = 0.05  # Wheel diameter in meters (example value)
WHEEL_BASE = 0.2  # Distance between wheels in meters (example value)

x_pos = 0.0  # Starting x position (bottom left)
y_pos = 0.0  # Starting y position (bottom left)
current_angle = 0.0  # Starting orientation

# Updated to match the number of state elements
state = namedtuple("state", ["us_sensor", "color_sensor", "color_sensor2", "g_sensor", "x_pos", "y_pos"])

global_state = Queue(maxsize=2)
global_enable = [True]*6  # Updated to match the number of state elements

us_sensor = Filtered_Sensor(us_sensor, Median_Filter(5))
th_engine = threads.ThreadEngine()

left_wheel = nav.wheel_left
right_wheel = nav.wheel_right

def get_state(enables=global_enable):
    return state(
        us_sensor.fetch() if enables[0] else "Disabled",
        color_sensor.fetch() if enables[1] else "Disabled",
        color_sensor2.fetch() if enables[2] else "Disabled",
        g_sensor.fetch() if enables[3] else "Disabled",
        x_pos if enables[4] else "Disabled",
        y_pos if enables[5] else "Disabled")

def calculate_position_update(left_speed, right_speed, current_angle):
    wheel_circumference = math.pi * WHEEL_DIAMETER
    left_linear_velocity = (left_speed / 360) * wheel_circumference
    right_linear_velocity = (right_speed / 360) * wheel_circumference
    
    # Translational and rotational velocities
    translational_velocity = (left_linear_velocity + right_linear_velocity) / 2
    rotational_velocity = (right_linear_velocity - left_linear_velocity) / WHEEL_BASE
    
    # Time step
    dt = 0.05
    
    angle_rad = math.radians(current_angle)
    dx = translational_velocity * math.cos(angle_rad) * dt
    dy = translational_velocity * math.sin(angle_rad) * dt
    
    d_angle = math.degrees(rotational_velocity * dt)
    
    return dx, dy, d_angle

def poll_sensors():
    global x_pos, y_pos, current_angle
    
    left_speed = left_wheel.get_speed()  # in dps
    right_speed = right_wheel.get_speed()  # in dps
    
    # Added current_angle parameter
    dx, dy, d_angle = calculate_position_update(left_speed, right_speed, current_angle)

    x_pos += dx
    y_pos += dy
    
    current_angle = (current_angle + d_angle) % 360

    global_state.put(get_state())
    
    time.sleep(0.05)

def start():
    th_engine.loop(poll_sensors)

def end():
    th_engine.join_all()
    reset_brick()