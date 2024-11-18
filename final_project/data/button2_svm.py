import pickle
import os
# load the weights from weights/button1_w.pkl

path = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(path, 'weights/button2_w.pkl'), 'rb') as f:
    weights = pickle.load(f)

def project(pixel, weight, bias):
    """
        return False for group0 and True for group1
    """

    res = weight[0] * pixel[0] + weight[1] * pixel[1] + weight[2] * pixel[2] + bias
    if res > 0:
        return False
    else:
        return True
"""
    decision_function = [
            ([green, blue, purple], [orange, red, yellow]),
            ([green], [purple, blue]),
            ([purple], [blue]),
            ([yellow], [orange, red]),
            ([orange], [red])
            ]
"""


def predict(pixel):
    if not project(pixel, weights[0][0], weights[0][1]):
        #green blue or purple
        if not project(pixel, weights[1][0], weights[1][1]):
            return 'g'
        else:
            if not project(pixel, weights[2][0], weights[2][1]):
                return 'p'
            else:
                return 'b'
    else:
        if not project(pixel, weights[3][0], weights[3][1]):
            return 'y'
        else:
            if not project(pixel, weights[4][0], weights[4][1]):
                return 'o'
            else:
                return 'r'

