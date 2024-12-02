import subsystem.car as car
from communication.client import Client
import time


c = car.Car()
# c.turn_left(100)

cl = Client()
try:
    while True:
        c.update(0.05)
        cl.send(( time.time(), c.state.us_sensor, c.state.us_sensor_2))
finally:
    cl.exit()