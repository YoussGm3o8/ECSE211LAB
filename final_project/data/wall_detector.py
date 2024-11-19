import csv
import numpy as np
import os
import matplotlib.pyplot as plt
from collections import deque
import statistics as stat

path = os.path.dirname(__file__)
path = os.path.join(path, "csv","simulated", "us_data.csv")
data = np.genfromtxt(path, delimiter=",", skip_header=1)

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


class Min_Filter(Filter):
    def __init__(self, buffer_length):
        super().__init__(min, buffer_length)

class Max_Filter(Filter):
    def __init__(self, buffer_length):
        super().__init__(max, buffer_length)

class EMA_Derivatives:
    def __init__(self, initial, alpha=0.1, bias=0):
        assert(len(initial) == 2)
        self.alpha = alpha
        self.prev = initial
        self.value = bias

    def update(self, current):
        delta_x = current[0] - self.prev[0]
        if abs(delta_x) < 1e-5:
            delta_x = 1e-5
        val = (current[1] - self.prev[1]) / (current[0] - self.prev[0])
        self.value = self.alpha * val + (1 - self.alpha) * self.value
        self.prev = current
        return self.value


med1 = Max_Filter(55)
med2 = Min_Filter(30)

data_med1 = np.array([(i[0], med1.update(i[1])) for i in data])
data_med2 = np.array([(i[0], med2.update(i[1])) for i in data])

plt.plot(data[:, 0], data[:, 1], c='g')
plt.plot(data_med2[:, 0], data_med2[:, 1], c='r')
plt.plot(data_med1[:, 0], data_med1[:, 1], c='b')
#show x axis on 0
plt.axhline(y=0, color='k')
plt.show()
