import subsystem.car as c
from common.filters import Diff
import time
from communication import client




car = c.Car()


car.forward(100)
try:
    while True:
        car.update(0.05)
        val =car.mini_scan()
        if (val is not None):
            print(val)
            car.stop()
            input("detected cube")
            car.forward(100)
finally:
    car.kill()