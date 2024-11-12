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
# load the weights from weights/button1_w.pkl

with open('weights/button1_w.pkl', 'rb') as f:
    weights = pickle.load(f)

"""decision_function = [
        ([green, blue], [orange, red, purple, yellow]),
        ([green], [blue]),
        ([orange, red], [purple, yellow]),
        ([purple], [yellow]),
        ([orange, yellow], [red]),
        ([yellow], [orange])
        ]

"""
def project(pixel, weight, bias):
    """
        return False for group0 and True for group1
    """

    res = weight[0] * pixel[0] + weight[1] * pixel[1] + weight[2] * pixel[2] + bias
    if res > 0:
        return True
    else:
        return False


def predict(pixel):
    if not project(pixel, weights[0][0], weights[0][1]):
        if not project(pixel, weights[1][0], weights[1][1]):
            return 'g'
        else:
            return 'b'
    elif project(pixel, weights[2][0], weights[2][1]) and not project(pixel, weights[3][0], weights[3][1]):
        return 'p'
    elif not project(pixel, weights[4][0], weights[4][1]):
        if not project(pixel, weights[5][0], weights[5][1]):
            return 'y'
        else:
            return 'o' 
    else:
        return 'r'
