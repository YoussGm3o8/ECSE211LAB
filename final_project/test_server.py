import communication.server as server
import components.engine as engine
import matplotlib.pyplot as plt
import time
from collections import deque
import csv
import os
import sys

x_points = deque(maxlen=2)
y_points = deque(maxlen=2)

buffer = []
if __name__ == "__main__":
    if len(sys.argv) != 2:
        path = None
    else:
        path = os.path.dirname(__file__)
        path = os.path.join(path, "data", "csv", sys.argv[1])

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
                buffer.append((t, message[1][0], message[1][1], message[1][2]))
                x_points.append(message[1][2])
                y_points.append(message[1][0])
                plt.plot(x_points, y_points, color='blue')
                if message[1][1]:
                    plt.axvline(t, color="red")
                plt.draw()
                plt.pause(0.05)
            elif message[0] == "row":
                t = time.time()
                buffer.append((t, message[1].us_sensor, message[1].g_sensor))
                plt.bar(t, message[1].us_sensor, color='green')
                plt.draw()
                plt.pause(0.05)

    finally:
        engine.end()
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
