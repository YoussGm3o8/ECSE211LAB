from utils.brick import EV3UltrasonicSensor
from common.filters import Median_Filter
# Constants
US_SENSOR_PORT = 1
FILTER_SIZE = 300 #size of filter for the median
SKIP_BATCH = 1

# Components

#WARNING: Do not handle None values here. Handle this in the robot logic loop
class US_Sensor(EV3UltrasonicSensor):
    def __init__(self, port):
        super().__init__(port)
        self.wait_ready()

    def fetch(self):
        return self.get_cm()

    def __iter__(self):
        while True:
            v = self.get_cm()
            if v is None:
                continue
            yield v

us_sensor = US_Sensor(US_SENSOR_PORT)
