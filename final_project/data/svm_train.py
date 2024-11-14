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
from color_numpy import green, blue, red, yellow, orange, purple
import pickle
import os

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
            ([green, blue, purple], [orange, red, yellow]),
            ([green], [purple, blue]),
            ([purple], [blue]),
            ([yellow], [orange, red]),
            ([orange], [red])
            ]

    for group0, group1 in decision_function:
        weight, bias = get_weight(group0, group1)
        button2_weights.append((weight, bias))


    #get path of this file directory
    path = os.path.dirname(os.path.abspath(__file__))
    output_location = os.path.join(path, "weights/button2_w.pkl")
    with open(output_location , 'wb') as f:
        pickle.dump(button2_weights, f)
        print("weights saved to ", output_location)

