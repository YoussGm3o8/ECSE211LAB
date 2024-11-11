from components.ultrasonic import us_sensor
from utils.brick import reset_brick

try:
    for data in us_sensor:
        print(data)
finally:
    reset_brick()
