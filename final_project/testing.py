import subsystem.car as c
from common.filters import Diff
import time
from communication import client


d = Diff(3, 1.5, 0.7)


cl = client.Client()
car = c.Car()


car.turn_left(50)
try:
    while True:
        car.update(0.05)
        data = 30 if car.state.us_sensor > 30 else car.state.us_sensor
        cl.send((time.time(), data))
        if d.update(time.time(), data):
            print("detected cube")
            car.stop()
            input("press enter to start again")
            car.turn_left(50)
finally:
    car.kill()