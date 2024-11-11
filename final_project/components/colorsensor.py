from utils.brick import EV3ColorSensor
from components.wrappers import Sensor
# Constants

COLOR_SENSOR_PORT = 2

# Components

class Color_Sensor(EV3ColorSensor, Sensor):
    def __init__(self, port):
        super().__init__(port)
        self.wait_ready()

    def fetch(self):
        if self.mode != self.Mode.COMPONENT:
            self.set_mode(self.Mode.COMPONENT)
            self.wait_ready()
        val = self.get_value() #DONT USE sensor.get_value() to get sensor data use this fetch method instead
        if val is None:
            raise TypeError("None caught")
        return val[:-1]

    def __iter__(self):
        while True:
            rgb = self.get_rgb()
            if rgb[0] is None:
                continue
            yield rgb


color_sensor = Color_Sensor(COLOR_SENSOR_PORT)

