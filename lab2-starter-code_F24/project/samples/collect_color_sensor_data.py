#!/usr/bin/env python3
import csv
import time
"""
This test is used to collect data from the color sensor.
It must be run on the robot.
"""

# Add your imports here, if any
from utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor, reset_brick


COLOR_SENSOR_DATA_FILE = "../data_analysis/color_sensor.csv"

# complete this based on your hardware setup
color_sensor = EV3ColorSensor(4) #TODO
touch_sensor = TouchSensor(3) #TODO

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.


def collect_color_sensor_data():
    "Collect color sensor data."
    try:
        with open(COLOR_SENSOR_DATA_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)            
            print("Press touch sensor to read color")
            
            while True:
                if touch_sensor.is_pressed():
                    rgb = color_sensor.get_rgb()
                    writer.writerow([rgb[0], rgb[1], rgb[2]])
                    print("Color recorded:", rgb)
                    time.sleep(0.01)
                    while touch_sensor.is_pressed():
                        time.sleep(0.01)
                        
    except KeyboardInterrupt:
        print("exit successful")
        file.close()
        exit()
        


if __name__ == "__main__":
    collect_color_sensor_data()
