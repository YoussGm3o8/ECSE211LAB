import csv
import numpy as np
import os
import matplotlib.pyplot as plt
from collections import deque
import statistics as stat

path = os.path.dirname(__file__)
path = os.path.join(path, "csv", "us_data4.csv")
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


class Median_Filter(Filter):
    def __init__(self, buffer_length):
        super().__init__(lambda x : stat.median(x), buffer_length)

class EMA_Derivatives:
    def __init__(self, initial, alpha=0.1):
        assert(len(initial) == 2)
        self.alpha = alpha
        self.prev = initial
        self.value = None

    def reset(self, initial):
        self.prev = initial
        self.value = None

    def update(self, current):
        delta_x = current[0] - self.prev[0]
        delta_y = current[1] - self.prev[1]
        #clamp delta_x
        if delta_x < 0.001 and delta_x >= 0:
            delta_x = 0.001
        elif delta_x > -0.001 and delta_x < 0:
            delta_x = -0.001

        val = delta_y / delta_x

        if self.value is None:
            self.value = val
        else:
            self.value = self.alpha * val + (1 - self.alpha) * self.value

        self.prev = current
        return self.value


dd = []
print(data.shape)
ema = EMA_Derivatives(data[0], alpha=0.55)
med = Median_Filter(10)
med2 = Median_Filter(2)
# median_data = [med.update(j[1] - i[1] / (j[0] - i[0])) for i, j in zip(data[:-1], data[1:])]
# plt.plot(data[1:, 0], median_data) 

data = np.array([(i[0], med2.update(i[1])) for i in data])
data = data[1:]

for i in data:
    dd.append(ema.update(i))

mean = np.mean(data[:, 1])

plt.plot(data[:, 0], dd, alpha=0.5)
#draw y lines where dd if within 0.1 of 0
# signal_detected = np.where(np.abs(dd) < 0.01, 1, 0)
last_detected = False
for i, j, coor in zip(dd[:-1], dd[1:], data[:-1, 0]):
    #if two adjacent values have different signs, then there is a signal
    if i * j < 0:
        if not last_detected:
            plt.axvline(x=coor, color='orange')
            last_detected = True
    #also if the value if within 0.1 of 0
    elif abs(i) < 0.01:
        if not last_detected:
            plt.axvline(x=coor, color='orange')
            last_detected = True
    else:
        last_detected = False


# plt.plot(data[:, 0], signal_detected, c='g')
plt.plot(data[:, 0], data[:, 1] - mean, alpha=1, c='r')
#show x axis on 0
plt.axhline(y=0, color='k')
plt.show()
