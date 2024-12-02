"""
Decision function: (based on priority)
g | b | p vs o | r | y
[if gbp]
g vs p | b
[if pb]
p vs b
[else ory]
y vs o | r
o vs r
"""
from sklearn import svm
import numpy as np
import pickle
import os

path = os.path.join(os.path.dirname(__file__), "csv", "color")
path = os.path.join(path, "sensor2")
print(path)

green = np.genfromtxt(os.path.join(path, "green.csv"), delimiter=',', skip_header=1)
blue = np.genfromtxt(os.path.join(path, "blue.csv"), delimiter=',', skip_header=1)
red = np.genfromtxt(os.path.join(path, "red.csv"), delimiter=',', skip_header=1)
yellow = np.genfromtxt(os.path.join(path, "yellow.csv"), delimiter=',', skip_header=1)
orange = np.genfromtxt(os.path.join(path, "orange.csv"), delimiter=',', skip_header=1)
purple = np.genfromtxt(os.path.join(path, "purple.csv"), delimiter=',', skip_header=1)
red2 = np.genfromtxt(os.path.join(path, "red_new.csv"), delimiter=',', skip_header=1)
red = np.concatenate((red, red2))
yellow2 = np.genfromtxt(os.path.join(path, "yellow_new.csv"), delimiter=',', skip_header=1)
yellow = np.concatenate((yellow, yellow2))

green = np.nan_to_num(green / np.repeat(np.sum(green, axis=1).reshape(-1, 1), 3, axis=1))
blue = np.nan_to_num(blue / np.repeat(np.sum(blue, axis=1).reshape(-1, 1), 3, axis=1))
red = np.nan_to_num(red / np.repeat(np.sum(red, axis=1).reshape(-1, 1), 3, axis=1))
yellow = np.nan_to_num(yellow / np.repeat(np.sum(yellow, axis=1).reshape(-1, 1), 3, axis=1))
orange = np.nan_to_num(orange / np.repeat(np.sum(orange, axis=1).reshape(-1, 1), 3, axis=1))
purple = np.nan_to_num(purple / np.repeat(np.sum(purple, axis=1).reshape(-1, 1), 3, axis=1))

def normalize(pixel):
    s = sum(pixel)
    if s == 0:
        return pixel
    return [i/s for i in pixel]

green = np.array([normalize(pixel) for pixel in green])
blue = np.array([normalize(pixel) for pixel in blue])
red = np.array([normalize(pixel) for pixel in red])
yellow = np.array([normalize(pixel) for pixel in yellow])
orange = np.array([normalize(pixel) for pixel in orange])
purple = np.array([normalize(pixel) for pixel in purple])


def get_weight(group0, group1):
    x1 = np.concatenate(group1)
    print(x1.shape)
    x2 = np.concatenate(group0)
    print(x2.shape)
    y1 = np.zeros(x1.shape[0])
    y2 = np.ones(x2.shape[0])

    clf = svm.LinearSVC()
    clf.fit(np.concatenate((x1, x2)), np.concatenate((y1, y2)).reshape(-1))
    w = []
    for i in clf.coef_.reshape(-1):
        w.append(float(i))
    #get the value of clf
    #print score accuracy
    print("accuracy: ", clf.score(np.concatenate((x1, x2)), np.concatenate((y1, y2)).reshape(-1)))
    return w, float(clf.intercept_[0])


if __name__ == '__main__':

    button2_weights = []

    decision_function = [
        ([green, blue, purple], [orange, red, yellow]),
        ([green], [purple, blue]),
        ([orange, red], [yellow])
        ]

    for group0, group1 in decision_function:
        weight, bias = get_weight(group0, group1)
        button2_weights.append((weight, bias))


    #get path of this file directory
    path = os.path.dirname(os.path.abspath(__file__))
    output_location = os.path.join(path, "weights/button2_w2.pkl")
    with open(output_location , 'wb') as f:
        pickle.dump(button2_weights, f)
        print("weights saved to ", output_location)

