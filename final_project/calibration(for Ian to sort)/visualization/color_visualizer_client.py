from common.wrappers import Normalized_Sensor
from common.normalization import RGB_Normalizer
from components.colorsensor import color_sensor
from utils.brick import reset_brick
from communication.client import Client
import time


cl = Client()

buffer = []

# sensor = Normalized_Sensor(color_sensor, RGB_Normalizer())

try:
    while True:
        time.sleep(0.1)
        # rgb = sensor.fetch()
        rgb = color_sensor.get_rgb()
        if rgb[0] is None:
            continue
        print(rgb, "raw")
        rgb = list(map(int, rgb))
        buffer.append(rgb)
        print(rgb, "int")
        if len(buffer) == 10:
            cl.send(buffer)
            buffer.clear()

except Exception as e:
    print(e)
finally:
    cl.exit()
    reset_brick()
