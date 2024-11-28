import communication.server as server
import matplotlib.pyplot as plt
import sys
from collections import deque
import numpy as np


xs = deque(maxlen=2)
ys = deque(maxlen=2)
ser = None
if len(sys.argv) != 2:
    print("Usage: python main_server.py <test name>")
    sys.exit(1)
try:
    ser = server.Server()
    color = {"forward_listen":"red", "refocus":"blue"}
    for message in ser:
        print(message[0], message)
        x = message[1][0]
        y = message[1][1]
        xs.append(x)
        ys.append(y)

        plt.plot(xs, ys, color[message[0]])
        plt.draw()
        plt.pause(0.05)
finally:
    if ser is not None:
        ser.exit()