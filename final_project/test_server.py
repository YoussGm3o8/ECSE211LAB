from communication.server import Server
import matplotlib.pyplot as plt



sv = Server()


try:
    for message in sv:
        plt.scatter(message[0], message[1], color="blue")

        plt.draw()
        plt.pause(0.05)
finally:
    sv.exit()

        