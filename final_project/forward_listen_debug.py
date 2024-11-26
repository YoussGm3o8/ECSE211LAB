import communication.server as server
import components.engine as engine
from components.engine import state
from main import FSM_state
import matplotlib.pyplot as plt
import os
import time
import tensorboard.summary as summary
import sys
from collections import deque
import numpy as np

#create tensorboard writer


writer = summary.Writer(os.path.join(os.path.dirname(__file__), "tensorboard"))
buffer = deque(maxlen=100)

if len(sys.argv) != 2:
    print("Usage: python main_server.py <test name>")
    sys.exit(1)

server = server.Server()
color = {"forward_listen":"red", "refocus":"blue"}
for message in server:
    print(message[0], message[1])
    t = time.time()
    writer.add_scalar(os.path.join(sys.argv[1], message[0]), t, message[1])
    buffer.append((t, message[1]))
    plt.bar(t, message[1], color=color[message[0]])
    plt.draw()
    plt.pause(0.05)

server.exit()