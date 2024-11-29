import subsystem.car as car
import time


c = car.Car()
is_slowed = False
c.forward(180)
ti = time.time()
while True:
    c.update()
    if c.detect_objects(15):
        is_slowed = True
        c.forward(100)

    if is_slowed and time.time() - ti > 2:
        c.forward(180)
        is_slowed = False
        ti = time.time()
    
    time.sleep(0.05)
    test_result = c.scan()
    if test_result is not None:
        print(test_result)
        break
    