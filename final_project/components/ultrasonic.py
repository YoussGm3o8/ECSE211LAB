from utils.brick import EV3UltrasonicSensor
from common.filters import Median_Filter
# Constants
US_SENSOR_PORT = 1
FILTER_SIZE = 300 #size of filter for the median
SKIP_BATCH = 1

# Components

#TODO: handle errors (None values) here
class US_Sensor(EV3UltrasonicSensor):
    def __init__(self, port):
        super().__init__(port)
        self.wait_ready()

    def fetch(self):
        # value = super().get_value() # NEVER USE sensor.get_value()
        value = self.get_cm()
        if value is None:
            raise TypeError("none caught")
        return value

    def __iter__(self):
        while True:
            v = self.get_cm()
            if v is None:
                #TODO: handle differently if needed
                continue
            yield v

us_sensor = US_Sensor(US_SENSOR_PORT)
