from collections.abc import Iterable
import statistics as stat
from collections import deque

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

    def extend(self, values : Iterable):
        self.buffer.extend(values)
        return self.func(self.buffer)

    def isReady(self):
        return len(self.buffer) == self.buffer.maxlen

    def __len__(self):
        return len(self.buffer)


class Median_Filter(Filter):
    def __init__(self, buffer_length):
        super().__init__(lambda x : stat.median(x), buffer_length)

class Mean_Filter(Filter):
    def __init__(self, buffer_length):
        super().__init__(lambda x : stat.mean(x), buffer_length)

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


