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
    return w, float(clf.intercept_[0])


if __name__ == '__main__':

    button1_weights = []
    decision_function = [
            ([green, blue], [orange, red, purple, yellow]),
            ([green], [blue]),
            ([orange, red], [purple, yellow]),
            ([purple], [yellow]),
            ([orange, yellow], [red]),
            ([yellow], [orange])
            ]

    for group1, group0 in decision_function:
        weight, bias = get_weight(group1, group0)
        button1_weights.append((weight, bias))


    #get path of this file directory
    path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(path, 'weights/button1_w.pkl'), 'wb') as f:
        pickle.dump(button1_weights, f)
        print("Weights saved in weights/button1_w.pkl")

