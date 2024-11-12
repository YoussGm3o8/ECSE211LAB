from components.colorsensor import color_sensor
from utils.brick import reset_brick

try:
    for data in color_sensor:
        print(color_sensor.predict(data))
finally:
    reset_brick()
