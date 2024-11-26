from communication.server import Server
import numpy as np
import matplotlib.pyplot as plt
# Function to draw a line from the origin with specified length and angle

# client_callback(("scan", (state.g_sensor, state.us_sensor, d.up, d.down, d.treshold, d.width)))
# Main loop
running = True
server = Server()

try:
    last = None
    axis_defined = False
    for message in server:
        if message[0] == "scan":

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


except Exception as e:
    print(e)
finally:
    server.exit()

