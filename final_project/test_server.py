"""
A set of scripts to test the brickpi using a server
"""


import communication.server as server
import components.engine as engine
import matplotlib.pyplot as plt
import time
import csv
import os
import sys

buffer = []
if __name__ == "__main__":
    if len(sys.argv) != 2:
        path = None
    else:
        path = os.path.dirname(__file__)
        path = os.path.join(path, "data", "csv", sys.argv[1])


    #CONSTANTS
    last = None
    axis_defined = False

    sv = server.Server()
    try:
        for message in sv:
            if message[0] == "test":
                t = time.time()
                buffer.append((t, message.us_sensor))
                plt.scatter(t, message.us_sensor, color='red')
                plt.draw()
                plt.pause(0.05)
            elif message[0] == "nav":
                t = time.time()
                buffer.append((t, message[1][0], message[1][1]))
                print(message[1][0])
                plt.bar(t, message[1][1], color='blue')
                plt.draw()
                plt.pause(0.05)
            elif message[0] == "row":
                t = time.time()
                buffer.append((t, message[1].us_sensor, message[1].g_sensor))
                plt.bar(t, message[1].us_sensor, color='green')
                plt.draw()
                plt.pause(0.05)
            elif message[0] == "scan":
                plt.scatter(message[1][0], message[1][1])
                if last is None:
                    last = message[1][1]
                else:
                    diff = message[1][1] - last
                    last = message[1][1]
                    plt.plot(message[1][0], diff)
                if len(message[1][2]) > 0:
                    up = message[1][2][-1]
                    plt.scatter(up[0], up[1], color='g')
                if len(message[1][3]) >0:
                    down = message[1][3][-1]
                    plt.scatter(down[0], down[1], color='b')

                if not axis_defined:
                    treshold = message[1][4]
                    alpha = message[1][5]
                    plt.axhline(y=treshold, color='r', linestyle='--')
                    plt.axhline(y=-treshold*alpha, color='r', linestyle='--')
                    axis_defined = True

                plt.draw()
                plt.pause(0.05)


    finally:
        engine.end()
        sv.exit()
        if path is not None:
            with open(path, "w") as f:
                w = csv.writer(f)
                for b in buffer:
                    w.writerow(b)


"""
Results:
Cone shape

cubes 16 cm apart center is aligned with left us_sensor eye
from left us_sensor eye lense -> 23 cm away

"""
