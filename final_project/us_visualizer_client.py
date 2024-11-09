from components.gyrosensor import g_sensor
from components.ultrasonic import us_sensor
from components.wrappers import Filtered_Sensor
from common.filters import Median_Filter, Mean_Filter
from utils.brick import reset_brick, wait_ready_sensors
import time
from communication.client import Client

FILTER_SIZE = 50
BATCH_SIZE = 5

cl = Client()
buffer = []
wait_ready_sensors(True)

us_sensor = Filtered_Sensor(us_sensor, Median_Filter(FILTER_SIZE))
g_sensor = Filtered_Sensor(g_sensor, Mean_Filter(FILTER_SIZE))

# try:
while True:
    for i in range(BATCH_SIZE):
        time.sleep(0.05)
        us_sensor.update()
        g_sensor.update()

    buffer.append((int(us_sensor.get()), int(g_sensor.get())))

    if len(buffer) == 50:
        cl.send(buffer)
        buffer.clear()
# except Exception as e:
#     print(e)
# finally:
#     cl.exit()
#     reset_brick()
