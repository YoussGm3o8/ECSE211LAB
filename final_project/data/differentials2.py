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
treshold = 40
print(data.shape)
avg = EMA(alpha=0.1)
ema = EMA_Derivatives(data[0], alpha=0.7)
med = Median_Filter(2)
# median_data = [med.update(j[1] - i[1] / (j[0] - i[0])) for i, j in zip(data[:-1], data[1:])]
# plt.plot(data[1:, 0], median_data) 

#process data
med_buf2 = []
med_buf = []
avg_buf = []
avg.reset(np.mean(data[:30,1]))
for x, y in data:
    y_m = med.update(y)
    y_a = avg.update(y)
    med_buf2.append((x, y_m))
    if y_m <= y_a:
        med_buf.append((x, y_m))
    else:
        med_buf.append((x, y_a))

    avg_buf.append((x, y_a))
dd = []

for i in med_buf:
    deriv = ema.update(i)
    dd.append(deriv)

def detection():
    signal_detected = 0
    down_signal = 0
    for i, j, d in zip(dd[:-1], dd[1:], data[1:]):
        if j < -0.3:
            down_signal = d[0]

        elif j > 0.3:
            if signal_detected > down_signal and signal_detected - down_signal < treshold:
                plt.axvline(x=signal_detected, color='r')
                signal_detected = 0

        if i * j < 0 and i < j:
            signal_detected = d[0]

detection()
med_buf = np.array(med_buf)
med_buf2 = np.array(med_buf2)

mean = np.mean(data[:, 1])
print(mean)
avg_buf = np.array(avg_buf)
plt.plot(avg_buf[:, 0], avg_buf[:, 1]-mean, alpha=1, c='b')
plt.plot(med_buf[:, 0], med_buf[:, 1]-mean, alpha=1, c='r')
plt.plot(med_buf[:, 0], np.array(dd), alpha=1, c='g')
plt.plot(med_buf2[:, 0], med_buf2[:, 1]-mean, alpha=1, c='y')
plt.axhline(y=0, color='k')
plt.show()
