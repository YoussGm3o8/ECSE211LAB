import communication.server as server
import components.engine as engine
import matplotlib.pyplot as plt
import time

if __name__ == "__main__":
    sv = server.Server()
    try:
        for message in sv:
            plt.scatter(time.time(), message.us_sensor)
            plt.draw()
            plt.pause(0.05)

    finally:
        engine.end()
# def scan_mean(client_callback=None):
