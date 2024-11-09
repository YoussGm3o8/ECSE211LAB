from common.filters import Filter

class Filtered_Sensor:
    def __init__(self, sensor , filter):
        assert(isinstance(filter, Filter))
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
