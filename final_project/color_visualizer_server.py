from communication.server import Server
import numpy as np
import matplotlib.pyplot as plt
from data.predictor.svm import colors, clf
# Function to draw a line from the origin with specified length and angle

# Main loop
running = True
server = Server()

try:
    for message in server:
        for rgb in message:
            if not running:
                break
            # print(rgb)
            pred = clf.predict([rgb])
            print(list(colors.keys())[list(colors.values()).index(pred[0])])
            plt.imshow(np.array(rgb).reshape((1,1,3)))
            #give delay
            plt.pause(0.05)
            plt.draw()
            plt.clf()

except Exception as e:
    print(e)
finally:
    server.exit()

