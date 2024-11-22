import numpy as np
import statistics as stat
import os
import matplotlib.pyplot as plt
from collections import deque
# Load your data (replace with correct path if needed)
path = os.path.dirname(__file__)
path = os.path.join(path, "csv", "rotate_around2.csv")
data = np.genfromtxt(path, delimiter=",", skip_header=1) 
data = data[:, 0:2]

class Filter:
    def __init__(self, func, buffer_length):
        self.buffer = deque(maxlen=buffer_length)
        self.func = func

    def update(self, value):
        """
        Update the buffer with the new value and returns the [func] of the buffer if full.

        NOTE: if the buffer is not full, the [func] is calculated based on the available values.

        *ASSUMES THAT VALUES ARE NOT NONE
        """
        self.buffer.append(value)
        return self.func(self.buffer)

    def extend(self, values):
        self.buffer.extend(values)
        return self.func(self.buffer)

    def isReady(self):
        return len(self.buffer) == self.buffer.maxlen

    def __len__(self):
        return len(self.buffer)


class Median_Filter(Filter):
    def __init__(self, buffer_length):
        super().__init__(lambda x : stat.median(x), buffer_length)

class Deriver:
    def __init__(self, treshold):
        self.treshold = treshold
        self.values = []

    def update(self, y):
        if len(self.values) == 0:
            self.values.append(y)
            return None
        diff = y - self.values[-1]
        self.values.append(y)
        if -self.treshold < diff < self.treshold:
            return 0
        return diff

class diff:
    def __init__(self, treshold, width, alpha):
        self.treshold = treshold
        self.up = []
        self.down = []
        self.values = []
        self.width = width
        self.alpha = alpha

    def update(self, x, y):
        if len(self.values) == 0:
            self.values.append(y)
            return False
        diff = y - self.values[-1]
        self.values.append(y)

        if diff > self.treshold:
            self.up.append((x,y))
            return self.is_signal()
        elif diff < -self.treshold * self.alpha:
            self.down.append((x,y))
        return False

    def is_signal(self):
        if len(self.up) > 0 and len(self.down) > 0:
            if abs(self.down[-1][0] - self.up[-1][0]) < self.width:
                return True
        return False

med = Median_Filter(5)
data = [(x, med.update(y)) for x, y in data[:]]
data = np.array(data)
dif = diff(16, 1.5, 0.7)
difference = []
ups = []
downs = []
for d in data:
    val = dif.update(d[0], d[1])
    if val:
        if dif.down[-1][1] < 50:
            difference.append(dif.down[-1])
            downs.append(dif.down[-1])
            ups.append(dif.up[-1])

for d in difference:
    plt.axvline(x=d[0], color='r')
plt.plot(data[:,0], data[:,1])

plt.show()
