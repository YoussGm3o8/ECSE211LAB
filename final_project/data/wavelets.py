import csv
import numpy as np
import os
import matplotlib.pyplot as plt
from collections import deque
import statistics as stat

path = os.path.dirname(__file__)
path = os.path.join(path, "csv", "us_data3.csv")
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

class EMA:
    def __init__(self, alpha=0.1):
        self.alpha = alpha
        self.value = None

    def reset(self, initial=None):
        self.value = initial

    def update(self, value):
        if self.value is None:
            self.value = value
        else:
            self.value = self.alpha * value + (1 - self.alpha) * self.value
        return self.value


def wavelet(x, h, w):
    """
        the full width of the wavelet is 3*w
    """

    if x >= h:
        if x < h + w:
            return -10 / w
        elif x < h + 2*w:
            return 30 / w
        elif x <= h + 3*w:
            return -10 / w
    return 0

def process_wavelets(data, width):
    tot = 0
    for d in data:
        tot += wavelet(d[0], data[0][0], width) * d[1]
    data = np.array(data)
    # plt.plot(data[:, 0], [wavelet(d[0], data[0][0], width) for d in data])
    # plt.plot(data[:, 0], [d[1] for d in data])
    # plt.scatter(data[0, 0], tot, c="blue")
    # plt.pause(0.05)
    # plt.draw()
    # plt.clf()
    return tot

class Wavelet_Filter(Filter):
    def __init__(self, buffer_len, width):
        super().__init__(lambda x : process_wavelets(x, width), buffer_len)

wa = Wavelet_Filter(20, 30)

print(data.shape)
mean = np.mean(data)
avg = EMA(alpha=0.1)
med = Median_Filter(15)
dema = EMA_Derivatives(data[0], alpha=0.55)
# data_processed = np.array([d[1] - avg.update(d[1]) for d in data])
data_processed = np.array([med.update(d[1]) for d in data])

dd = []
for i in data:
    dd.append(dema.update(i))

data = np.array(data)
wavelet_graph = np.array([(i[0], wa.update(i)) for i in zip(data[:,0], data_processed)])

plt.plot(data[:, 0], wavelet_graph[:, 1], c='g')
plt.plot(data[:, 0], data_processed)
#plot 0 axis
plt.axhline(0, color='black', lw=1)
plt.show()

