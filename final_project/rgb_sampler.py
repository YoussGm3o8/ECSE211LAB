from components.color import color_sensor as cs
from utils.brick import reset_brick
import numpy as np
import matplotlib.pyplot as plt
import time

try:
    while(True):
        data = cs.fetch()
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
