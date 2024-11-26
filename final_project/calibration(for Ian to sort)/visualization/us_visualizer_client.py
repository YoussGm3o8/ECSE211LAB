from components.gyrosensor import g_sensor
from components.ultrasonic import us_sensor
from common.wrappers import Filtered_Sensor
from common.filters import Median_Filter, Mean_Filter
import time
from utils.brick import reset_brick
from communication.client import Client

FILTER_SIZE = 50
BATCH_SIZE = 5

cl = Client()
buffer = []

us_sensor = Filtered_Sensor(us_sensor, Median_Filter(FILTER_SIZE))

try:
    while True:
        for i in range(BATCH_SIZE):
            time.sleep(0.05)
            us_sensor.update()

        buffer.append((int(us_sensor.get()), int(g_sensor.fetch())))

        if len(buffer) == 10:
            cl.send(buffer)
            buffer.clear()
except Exception as e:
    print(e)
finally:
    cl.exit()
    reset_brick()
