from components.gyrosensor import g_sensor
from utils.brick import reset_brick, wait_ready_sensors

wait_ready_sensors(True)
try:
    for data in g_sensor:
        print(data)
finally:
    reset_brick()
