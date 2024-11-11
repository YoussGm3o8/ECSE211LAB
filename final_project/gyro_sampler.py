from components.gyrosensor import g_sensor
from utils.brick import reset_brick

try:
    for data in g_sensor:
        print(data)
finally:
    reset_brick()
