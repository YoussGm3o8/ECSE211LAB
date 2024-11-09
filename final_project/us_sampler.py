from components.ultrasonic import us_sensor
from utils.brick import reset_brick, wait_ready_sensors

wait_ready_sensors(True)
try:
    for data in us_sensor:
        print(data)
finally:
    reset_brick()
