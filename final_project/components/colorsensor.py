from utils.brick import EV3ColorSensor
from components.wrappers import Normalized_Sensor
from common.normalization import RGB_Normalizer
from data.button1_svm import predict
# Constants

COLOR_SENSOR_PORT = 2

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
            return None
        return val[:-1]
    
    def predict(self):
        pred = predict(self.fetch())
        while pred is None:
            pred = predict(self.fetch())
        return pred

    def __iter__(self):
        while True:
            rgb = self.get_rgb()
            if rgb[0] is None:
                continue
            yield rgb

color_sensor = Color_Sensor(COLOR_SENSOR_PORT) 
