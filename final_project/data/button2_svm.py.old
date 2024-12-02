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
        return True
    else:
        return False

"""
    decision_function = [
            ([white, green, blue, purple], [orange, red, yellow]),
            ([green], [purple, blue, white]),
            ([purple, white], [blue]),
            ([purple], [white]),
            ([yellow], [orange, red]),
            ([orange], [red])
            ]
"""

def is_unknown(pixel, treshold=1150):
    dist = pixel[0] ** 2 + pixel[1] ** 2 + pixel[2] ** 2
    return dist < treshold

def normalize(pixel):
    s = sum(pixel)
    if s == 0:
        return pixel
    return [i/s for i in pixel]

def predict(pixel):
    str = ""
    if is_unknown(pixel, 2400):
        str += "u"

    pixel = normalize(pixel)

    if project(pixel, weights[0][0], weights[0][1]):
        #green blue or purple
        if project(pixel, weights[1][0], weights[1][1]):
            return str+'g'
        else:
            if project(pixel, weights[2][0], weights[2][1]):
                if project(pixel, weights[3][0], weights[3][1]):
                    return str+'p'
                else:
                    return str+'w'
            else:
                return str+'b'
    else:
        if project(pixel, weights[4][0], weights[4][1]):
            return str+'y'
        else:
            if project(pixel, weights[5][0], weights[5][1]):
                return str+'o'
            else:
                return str+'r'

