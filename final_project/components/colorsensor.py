from utils.brick import EV3ColorSensor
from components.wrappers import Normalized_Sensor
from common.normalization import RGB_Normalizer
from data.button1_svm import predict
# Constants

LEFT_COLOR_SENSOR_PORT = 3
RIGHT_COLOR_SENSOR_PORT = 2

# Components

class Color_Sensor(EV3ColorSensor):
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

    def predict(self, raw_rgb):
        return predict(raw_rgb)

    def __iter__(self):
        while True:
            rgb = self.get_rgb()
            if rgb[0] is None:
                continue
            yield rgb

color_sensor = Color_Sensor(RIGHT_COLOR_SENSOR_PORT) 
left_color_sensor = Color_Sensor(LEFT_COLOR_SENSOR_PORT) 
