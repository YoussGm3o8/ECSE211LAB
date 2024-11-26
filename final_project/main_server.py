import communication.server as server
import components.engine as engine
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
    print("Usage: python main_server.py <port>")
    sys.exit(1)

server = server.Server()

for message in server():
    t = time.time()
    writer.add_scalar(os.path.join(sys.argv[1], message.state), t, message.arguments.us_sensor)
    buffer.append((t, message.arguments.us_sensor))
    buf = np.array(buffer)
    plt.plot(buf[:, 0], buf[:, 1], color="b")
    plt.draw()
    plt.clf()
    plt.pause(0.05)

server.exit()