from components.wrappers import Normalized_Sensor
from common.normalization import RGB_Normalizer
from components.colorsensor import color_sensor


sensor = Normalized_Sensor(color_sensor, RGB_Normalizer())

