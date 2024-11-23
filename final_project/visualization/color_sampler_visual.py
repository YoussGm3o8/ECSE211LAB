"""
This script is used to sample the color sensor and save the data to a csv file
It requires color_visualizer_server.py to be running your computer to visualize the data
"""

from components.colorsensor import color_sensor
from utils.brick import reset_brick
from communication.client import Client
import time
import sys
import os
import csv

if len(sys.argv) < 2:
    print("missing output_file argument")
    sys.exit(1)

cl = Client()

buffer = []
buffer_file = []

try:
    for i, rgb in enumerate(color_sensor):
        print(color_sensor.predict(rgb))
        time.sleep(0.05)
        rgb = list(map(int, rgb))
        buffer.append(rgb)
        buffer_file.append(rgb)
        if len(buffer) == 10:
            cl.send(buffer)
            buffer.clear()
        if len(buffer_file) >= 1000:
            break

except Exception as e:
    print(e)
finally:
    cl.exit()
    reset_brick()
    path = os.path.join(os.path.dirname(__file__), sys.argv[1])
    with open(path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(buffer_file)

