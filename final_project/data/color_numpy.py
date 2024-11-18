import numpy as np
import matplotlib.pyplot as plt
import os

os_main = None
if __name__ != "__main__":
    os_main = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

#open green.csv to numpy
path = os.path.join(os.path.dirname(__file__), "csv", "color")
path = os.path.join(path, "sensor2")
print(path)
green = np.genfromtxt(os.path.join(path, "green.csv"), delimiter=',', skip_header=1)
blue = np.genfromtxt(os.path.join(path, "blue.csv"), delimiter=',', skip_header=1)
red = np.genfromtxt(os.path.join(path, "red.csv"), delimiter=',', skip_header=1)
yellow = np.genfromtxt(os.path.join(path, "yellow.csv"), delimiter=',', skip_header=1)
orange = np.genfromtxt(os.path.join(path, "orange.csv"), delimiter=',', skip_header=1)
purple = np.genfromtxt(os.path.join(path, "purple.csv"), delimiter=',', skip_header=1)

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
    from button2_svm import predict
    print(purple.shape)
    #scatter plot 3d
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(blue_norm[:,0], blue_norm[:,1], blue_norm[:,2], c='b', marker='o', label='blue')
    ax.scatter(red_norm[:,0],red_norm[:,1], red_norm[:,2], c='r', marker='o', label='red')
    ax.scatter(yellow_norm[:,0], yellow_norm[:,1], yellow_norm[:,2], c='y', marker='o', label='yellow')
    ax.scatter(orange_norm[:,0], orange_norm[:,1], orange_norm[:,2], c='orange', marker='o', label='orange')
    ax.scatter(purple_norm[:,0], purple_norm[:,1], purple_norm[:,2], c='purple', marker='o', label='purple')
    ax.scatter(green_norm[:,0], green_norm[:,1], green_norm[:,2], c='g', marker='o', label='green')
    plt.show()

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
        if predict(pixel) == 'g':
            green_correct += 1
    for pixel in blue:
        if predict(pixel) == 'b':
            blue_correct += 1
    for pixel in red:
        if predict(pixel) == 'r':
            red_correct += 1
    for pixel in yellow:
        v = predict(pixel)
        if v == 'y':
            yellow_correct += 1
    for pixel in orange:
        if predict(pixel) == 'o':
            orange_correct += 1
    for pixel in purple:
        if predict(pixel) == 'p':
            purple_correct += 1
    print("Green: ", green_correct/green.shape[0])
    print("Blue: ", blue_correct/blue.shape[0])
    print("Red: ", red_correct/red.shape[0])
    print("Yellow: ", yellow_correct/yellow.shape[0])
    print("Orange: ", orange_correct/orange.shape[0])
    print("Purple: ", purple_correct/purple.shape[0])
    import svm
    # now do the same using svm.clf
    green_correct = 0
    blue_correct = 0
    red_correct = 0
    yellow_correct = 0
    orange_correct = 0
    purple_correct = 0
    for pixel in green:
        if svm.clf.predict([pixel])[0] == 0:
            green_correct += 1
    for pixel in blue:
        if svm.clf.predict([pixel])[0] == 1:
            blue_correct += 1
    for pixel in red:
        if svm.clf.predict([pixel])[0] == 2:
            red_correct += 1
    for pixel in yellow:
        if svm.clf.predict([pixel])[0] == 3:
            yellow_correct += 1
    for pixel in orange:
        if svm.clf.predict([pixel])[0] == 4:
            orange_correct += 1
    for pixel in purple:
        if svm.clf.predict([pixel])[0] == 5:
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
