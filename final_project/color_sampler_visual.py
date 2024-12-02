"""
This script is used to sample the color sensor and save the data to a csv file
It requires color_visualizer_server.py to be running your computer to visualize the data
"""

from utils.brick import reset_brick
from communication.client import Client
from common.constants_params import *
from utils.brick import EV3ColorSensor
import time
import sys
import os
import csv

if len(sys.argv) < 2:
    print("missing output_file argument")
    sys.exit(1)

cl = Client()
sensor = EV3ColorSensor(COLOR_SENSOR)
buffer = []
buffer_file = []

try:
    for i in range(500):
        time.sleep(0.05)
        rgb = sensor.get_rgb()
        if rgb[0] is not None:
            print(rgb)
            rgb = list(map(int,rgb))
            buffer.append(rgb)
            buffer_file.append(rgb)
            if len(buffer) == 10:
                cl.send(buffer)
                buffer.clear()

except Exception as e:
    print(e)
finally:
    cl.exit()
    reset_brick()
    path = os.path.join(os.path.dirname(__file__), sys.argv[1])
    with open(path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(buffer_file)

