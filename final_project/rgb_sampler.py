from components.color_detection import color_sensor as cs
from utils.brick import reset_brick, wait_ready_sensors
import numpy as np
import matplotlib.pyplot as plt
import time

try:
    wait_ready_sensors(True)
    while(True):
        data = cs.get_rgb()
        try:
            plt.imshow(np.array(data).reshape((1,1,3)))
            #give delay
            plt.pause(0.05)
            plt.draw()
            plt.clf()
        except Exception:
            print(Exception)
        time.sleep(0.05)

        #user exit exception
except KeyboardInterrupt:
    #this only catches Ctrl+C (not Ctrl+z)
    reset_brick()
