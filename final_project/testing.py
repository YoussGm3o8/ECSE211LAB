import subsystem.car as c
from common.filters import Diff
import time
from communication import client


d = Diff(3, 1.5, 0.7)


cl = client.Client()
car = c.Car()


try:
    while True:
        car.update(0.05)
        data = car.state.us_sensor_2
        print(car.state.us_sensor, car.state.us_sensor_2)
        cl.send((time.time(), data))
finally:
    car.kill()
