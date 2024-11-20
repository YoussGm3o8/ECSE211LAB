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

