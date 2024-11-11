from common.filters import Filter
from common.normalization import Normalizer

class Sensor:
    def fetch(self):
        raise NotImplementedError("fetch method not implemented")


class Filtered_Sensor:
    def __init__(self, sensor , filter):
        assert(isinstance(filter, Filter))
        assert(isinstance(sensor, Sensor))
        self.sensor = sensor
        self.filter = filter
        self.buffer = [] # this buffer is used to filter in batches

    def update(self):
        self.buffer.append(self.sensor.fetch())

    def get(self):
        value = self.filter.extend(self.buffer)
        self.buffer.clear()
        return value

    def get_value(self):
        return self.filter.update(self.sensor.fetch())


class Normalized_Sensor:
    def __init__(self, sensor, normalizer):
        assert(isinstance(normalizer, Normalizer))
        assert(isinstance(sensor, Sensor))
        self.sensor = sensor
        self.normalizer = normalizer

    def get_value(self):
        return self.normalizer.normalize(self.sensor.fetch())

