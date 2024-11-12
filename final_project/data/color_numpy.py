import numpy as np
import matplotlib.pyplot as plt
import os

os_main = None
if __name__ != "__main__":
    os_main = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
else:
    import button1_svm

#open green.csv to numpy

green = np.genfromtxt('csv/green.csv', delimiter=',', skip_header=1)
blue = np.genfromtxt('csv/blue.csv', delimiter=',', skip_header=1)
red = np.genfromtxt('csv/red.csv', delimiter=',', skip_header=1)
yellow = np.genfromtxt('csv/yellow.csv', delimiter=',', skip_header=1)
orange = np.genfromtxt('csv/orange.csv', delimiter=',', skip_header=1)
purple = np.genfromtxt('csv/purple.csv', delimiter=',', skip_header=1)


def normalize(data):
    s = data.sum(axis=1).reshape(-1, 1)
    data = data/s
    data = data[~np.isnan(data).any(axis=1)]
    return data

green_norm = normalize(green)
blue_norm = normalize(blue)
red_norm = normalize(red)
yellow_norm = normalize(yellow)
orange_norm = normalize(orange)
purple_norm = normalize(purple)

if __name__ == "__main__":
    print(purple.shape)
    #scatter plot 3d
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(green[:,0], green[:,1], green[:,2], c='g', marker='o', label='green')
    ax.scatter(blue[:,0], blue[:,1], blue[:,2], c='b', marker='o', label='blue')
    ax.scatter(red[:,0], red[:,1], red[:,2], c='r', marker='o', label='red')
    ax.scatter(yellow[:,0], yellow[:,1], yellow[:,2], c='y', marker='o', label='yellow')
    ax.scatter(orange[:,0], orange[:,1], orange[:,2], c='orange', marker='o', label='orange')
    ax.scatter(purple[:,0], purple[:,1], purple[:,2], c='purple', marker='o', label='purple')
    plt.show()

    #measure accuracy of button1_svm.predict(pixel)
    green_correct = 0
    blue_correct = 0
    red_correct = 0
    yellow_correct = 0
    orange_correct = 0
    purple_correct = 0
    for pixel in green:
        if button1_svm.predict(pixel) == 'g':
            green_correct += 1
    for pixel in blue:
        if button1_svm.predict(pixel) == 'b':
            blue_correct += 1
    for pixel in red:
        if button1_svm.predict(pixel) == 'r':
            red_correct += 1
    for pixel in yellow:
        v = button1_svm.predict(pixel)
        if v == 'y':
            yellow_correct += 1
    for pixel in orange:
        if button1_svm.predict(pixel) == 'o':
            orange_correct += 1
    for pixel in purple:
        if button1_svm.predict(pixel) == 'p':
            purple_correct += 1
    print("Green: ", green_correct/green.shape[0])
    print("Blue: ", blue_correct/blue.shape[0])
    print("Red: ", red_correct/red.shape[0])
    print("Yellow: ", yellow_correct/yellow.shape[0])
    print("Orange: ", orange_correct/orange.shape[0])
    print("Purple: ", purple_correct/purple.shape[0])



else:
    #reset the root directory to the original
    if os_main is not None:
        os.chdir(os_main)
