import numpy as np
import statistics as stat
import os
import matplotlib.pyplot as plt
from collections import deque
# Load your data (replace with correct path if needed)
path = os.path.dirname(__file__)
path = os.path.join(path, "csv", "move_up_row2.csv")
#open file and read data
#data format:
# 1732227866.73126,"state(us_sensor=97.6, color_sensor='unknown', color_sensor2='unknown', g_sensor=-504)"
# 1732227867.1541207,"state(us_sensor=97.6, color_sensor='unknown', color_sensor2='unknown', g_sensor=-508)"
# 1732227867.2320251,"state(us_sensor=97.6, color_sensor='unknown', color_sensor2='unknown', g_sensor=-537)"

with open(path, 'r') as f:
    data = f.readlines()
    data = [d.split(",") for d in data]
    # data = [(float(d[0]), float(d[1].split("state(us_sensor=")[0])) for d in data]
    data = [(float(d[0]), float(d[1].split("state(us_sensor=")[1].split(",")[0])) for d in data]
    data = np.array(data)

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

der = Deriver(5)
med = Median_Filter(5)
data = [(x, med.update(y)) for x, y in data[:]]
data = np.array(data)
difference = [der.update(y) for y in data[:, 1]]
difference = np.array(difference)[1:]
marks = np.array(np.where(difference > 0)).reshape(-1)
for m in marks:
    print(m)
    plt.axvline(x=data[m][0], color='r')
print(marks)

plt.plot(data[:,0], data[:,1])
plt.plot(data[1:,0], difference)
plt.show()

