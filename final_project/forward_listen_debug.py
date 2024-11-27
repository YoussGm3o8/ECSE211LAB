import communication.server as server
import components.engine as engine
from components.engine import state
from main import FSM_state
import matplotlib.pyplot as plt
import sys
from collections import deque
import numpy as np


xs = deque(maxlen=2)
ys = deque(maxlen=2)

if len(sys.argv) != 2:
    print("Usage: python main_server.py <test name>")
    sys.exit(1)
try:
    server = server.Server()
    color = {"forward_listen":"red", "refocus":"blue"}
    for message in server:
        print(message[0], message)
        x = message[1][0]
        y = message[1][0]
        xs.append(x)
        ys.append(y)

        plt.plot(xs, ys, color[message[0]])
        plt.draw()
        plt.pause(0.05)
finally:
    server.exit()