from utils.brick import EV3UltrasonicSensor
from common.filters import Median_Filter
#WARNING: Do not handle None values here. Handle this in the robot logic loop
class US_Sensor(EV3UltrasonicSensor):
    def __init__(self, port):
        super().__init__(port)
        print(f"waiting for US on port {port}")
        self.set_mode(self.Mode.CM)
        self.wait_ready()

    def __str__(self):
        return f"US_Sensor(port={self.port})"

    def fetch(self):
        return self.get_value()
