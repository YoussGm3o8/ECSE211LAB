from utils.brick import EV3GyroSensor

GYRO_PORT = 4

class GYRO_Sensor(EV3GyroSensor):
    def __init__(self, port):
        super().__init__(port)
        self.wait_ready()

    def fetch(self):
        value = super().get_abs_measure()
        if value is None:
            raise TypeError("None caught")
        return value
    
    def __iter__(self):
        """
        Change gyro sensor mode.

        abs - Absolute degrees rotated since start
        dps - Degrees per second of rotation
        both - list of [abs, dps] values

        NOTE: __iter__ returns both
        """
        while True:
            values = self.get_both_measure()
            if values is None:
                #TODO: handle differently if needed
                continue
            yield values

g_sensor = GYRO_Sensor(GYRO_PORT)
