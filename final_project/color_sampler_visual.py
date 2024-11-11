from components.colorsensor import color_sensor
from utils.brick import reset_brick
from communication.client import Client
from communication.csvwritter import to_csv
import time
cl = Client()

buffer = []
buffer_file = []

try:
    for i, rgb in enumerate(color_sensor):
        time.sleep(0.05)

        print(rgb, "raw")
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
    to_csv(buffer_file)
