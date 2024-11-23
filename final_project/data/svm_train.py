"""
the script used to train the SVM models weigth for the color sensors
"""


from sklearn import svm
import numpy as np
import pickle
import os

path = os.path.join(os.path.dirname(__file__), "csv", "color")
# path = os.path.join(path, "sensor2")
print(path)

green = np.genfromtxt(os.path.join(path, "green.csv"), delimiter=',', skip_header=1)
blue = np.genfromtxt(os.path.join(path, "blue.csv"), delimiter=',', skip_header=1)
red = np.genfromtxt(os.path.join(path, "red.csv"), delimiter=',', skip_header=1)
yellow = np.genfromtxt(os.path.join(path, "yellow.csv"), delimiter=',', skip_header=1)
orange = np.genfromtxt(os.path.join(path, "orange.csv"), delimiter=',', skip_header=1)
purple = np.genfromtxt(os.path.join(path, "purple.csv"), delimiter=',', skip_header=1)
white = np.genfromtxt(os.path.join(path, "white.csv"), delimiter=',', skip_header=1)

green = np.nan_to_num(green / np.repeat(np.sum(green, axis=1).reshape(-1, 1), 3, axis=1))
blue = np.nan_to_num(blue / np.repeat(np.sum(blue, axis=1).reshape(-1, 1), 3, axis=1))
red = np.nan_to_num(red / np.repeat(np.sum(red, axis=1).reshape(-1, 1), 3, axis=1))
yellow = np.nan_to_num(yellow / np.repeat(np.sum(yellow, axis=1).reshape(-1, 1), 3, axis=1))
orange = np.nan_to_num(orange / np.repeat(np.sum(orange, axis=1).reshape(-1, 1), 3, axis=1))
purple = np.nan_to_num(purple / np.repeat(np.sum(purple, axis=1).reshape(-1, 1), 3, axis=1))
white = np.nan_to_num(white / np.repeat(np.sum(white, axis=1).reshape(-1, 1), 3, axis=1))

def get_weight(group0, group1):
    x1 = np.array(group1).reshape((-1, 3))
    x2 = np.array(group0).reshape((-1, 3))
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
        ([green, blue], [white, orange, red, purple, yellow]),
        ([green], [blue]),
        ([orange, red, yellow], [purple, white]),
        ([purple], [white]),
        ([orange, red], [yellow]),
        ([orange], [red])
        ]

    # decision_function = [
    #         ([white, green, blue, purple], [orange, red, yellow]),
    #         ([green], [purple, blue, white]),
    #         ([purple, white], [blue]),
    #         ([purple], [white]),
    #         ([yellow], [orange, red]),
    #         ([orange], [red])
    #         ]

    for group0, group1 in decision_function:
        weight, bias = get_weight(group0, group1)
        button2_weights.append((weight, bias))


    #get path of this file directory
    path = os.path.dirname(os.path.abspath(__file__))
    output_location = os.path.join(path, "weights/button1_w.pkl")
    with open(output_location , 'wb') as f:
        pickle.dump(button2_weights, f)
        print("weights saved to ", output_location)

