from utils.brick import EV3ColorSensor
from common.wrappers import Normalized_Sensor
from common.normalization import RGB_Normalizer
from data.button1_svm import predict
#from deprecated import deprecated
# Constants

COLOR_SENSOR_PORT = 2

# Components

#WARNING: Do not handle None values here. Handle this in the robot logic loop
class Color_Sensor(EV3ColorSensor):
    def __init__(self, port):
        super().__init__(port)
        self.wait_ready()

    def __str__(self):
        return f"Color_Sensor(port={self.port})"

    def fetch(self):
        if self.mode != self.Mode.COMPONENT:
            self.set_mode(self.Mode.COMPONENT)
            self.wait_ready()
        val = self.get_value() #DONT USE sensor.get_value() to get sensor data use this fetch method instead
        if val is None:
            return None
        return predict(val[:-1])

    #@deprecated(reason="This function is unsafe because it hides None values from caller. Use fetch instead.")
    def predict(self, value=None):
        if value is not None:
            return predict(value)
        v = self.fetch()
        while v is None:
            v = self.fetch()
        return v

    def __iter__(self):
        while True:
            rgb = self.get_rgb()
            if rgb[0] is None:
                continue
            yield rgb

color_sensor = Color_Sensor(COLOR_SENSOR_PORT) 
