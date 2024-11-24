from common.filters import Filter
from common.normalization import Normalizer

class Filtered_Sensor:
    def __init__(self, sensor , filter):
        assert(isinstance(filter, Filter))
        self.sensor = sensor
        self.filter = filter
        self.buffer = [] # this buffer is used to filter in batches

    def update(self):
        """
        returns: True if the buffer has successfully updated
        False, otherwise.
        """
        v = self.sensor.fetch()
        if v is None:
            return False
        self.buffer.append(v)
        return True

    def get(self):
        """
        NOTE: Use the update() method output to check if the buffer has been updated.
        Otherwise, you will get the same values.
        """
        value = self.filter.extend(self.buffer)
        self.buffer.clear()
        return value

    def fetch(self):
        v = self.sensor.fetch()
        if v is None:
            return None
        return self.filter.update(v)

class Filtered_Sensor_V2(Filtered_Sensor):
    """
    Provides the raw value of the sensor in cases needed
    """
    def __init__(self, sensor, filter):
        super().__init__(sensor, filter)
    def fetch(self):
        v = self.sensor.fetch()
        if v is None:
            return None, None
        return self.filter.update(v), v

class Normalized_Sensor:
    def __init__(self, sensor, normalizer):
        assert(isinstance(normalizer, Normalizer))
        self.sensor = sensor
        self.normalizer = normalizer

    def fetch(self):
        v = self.sensor.fetch()
        if v is None:
            return None
        return self.normalizer.normalize(v)

class US_Sensor_High_PollingRate:
    def __init__(self, sensor):
        self.sensor = sensor
        self.last = None
    
    def fetch(self):
        current = self.sensor.fetch()
        if current != self.last:
            self.last = current
            return current
        return None

class US_Sensor_High_PollingRate_V2(US_Sensor_High_PollingRate):
    def __init__(self, sensor):
        super().__init__(sensor)

    def fetch(self):
        current = self.sensor.fetch()
        if current[0] != self.last[0]:
            self.last = current
            return current
        return None, None