import numpy as np
import statistics as stat
import os
import matplotlib.pyplot as plt
from collections import deque

# Load your data (replace with correct path if needed)
path = os.path.dirname(__file__)
path = os.path.join(path, "csv", "us_data3.csv")
data = np.genfromtxt(path, delimiter=",", skip_header=1)
diffs = np.diff(data[:, 1])
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



class diff:
    def __init__(self, treshold, width):
        self.treshold = treshold
        self.up = []
        self.down = []
        self.values = []
        self.width = width

    def update(self, x, y):
        if len(self.values) == 0:
            self.values.append(y)
            return False
        diff = y - self.values[-1]
        self.values.append(y)

        if diff > self.treshold:
            self.up.append((x,y))
            return self.is_signal()
        elif diff < -self.treshold:
            self.down.append((x,y))
        return False

    def is_signal(self):
        if len(self.up) > 0 and len(self.down) > 0:
            if abs(self.down[-1][0] - self.up[-1][0]) < self.width:
                return True
        return False


# filter = Median_Filter(1)
# data = np.array([(x, filter.update(y)) for x, y in data[:]])

d = diff(4, 40)

vars = []
var = 0
mean = 0
diffs = np.diff(data[:,1]).reshape(-1, 1)
for i, di in enumerate(diffs):
    mean = mean - (mean - di) / (i +1) 
    var = var - (var - (di - mean) ** 2) * 0.2 
    vars.append(var)
print(mean, np.mean(diffs))
plt.plot(data[1:, 0], vars)


signals = []
for s in data:
    new_d = d.update(s[0], s[1])
    if (new_d):
        plt.axvline(x=d.down[-1][0], color='r', linestyle='--')

#plot data

plt.plot(data[:,0], data[:,1])
plt.plot(data[1:,0], diffs)

ups = np.array(d.up).reshape(-1, 2)
downs = np.array(d.down).reshape(-1, 2)
plt.scatter(ups[:,0], ups[:,1], color='g')
plt.scatter(downs[:,0], downs[:,1], color='b')
plt.show()

