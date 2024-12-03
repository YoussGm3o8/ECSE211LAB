"""
Decision function: (based on priority)
- g|b vs other
    -g v b
[if other]
- o | r vs p
-p vs y
[if not both p]
- o | y vs r
    - y vs o
"""

import pickle
import os
# load the weights from weights/button1_w.pkl

path = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(path, 'weights/button1_w2.pkl'), 'rb') as f:
    weights = pickle.load(f)

"""
true -> first element
false -> second element
    
"""
# decision_function = [
#         ([green, blue, purple], [orange, red, yellow]),
#         ([green], [purple, blue]),
#         ([orange, red], [yellow])
#         ]

def project(pixel, weight, bias):
    """
        return False for group0 and True for group1
    """

    res = weight[0] * pixel[0] + weight[1] * pixel[1] + weight[2] * pixel[2] + bias
    if res > 0:
        return True
    else:
        return False


def is_unknown(pixel, treshold=1150):
    dist = pixel[0] ** 2 + pixel[1] ** 2 + pixel[2] ** 2
    return dist < treshold

def normalize(pixel):
    s = sum(pixel)
    if s == 0:
        return pixel
    return [i/s for i in pixel]


def predict(pixel):
    c = ""
    if is_unknown(pixel, 2600):
        c += "u"

    pixel = normalize(pixel)

    if project(pixel, weights[0][0], weights[0][1]):
        if (project(pixel, weights[1][0], weights[1][1])):
            return c+'g'
        else:
            return c+'b'
    else:
        if project(pixel, weights[2][0], weights[2][1]):
            return c+'o'
        else:
            return c+'y'
