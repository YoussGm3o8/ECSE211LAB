from utils.brick import EV3GyroSensor
import time

GYRO_PORT = 4


#WARNING: Do not handle None values here. Handle this in the robot logic loop
class GYRO_Sensor(EV3GyroSensor):
    def __init__(self, port):
        super().__init__(port)
        self.wait_ready()

    def __str__(self):
        return f"GYRO_Sensor(port={self.port})"

    def fetch(self):
        return self.get_abs_measure()

    def reset(self):
        self.reset_measure()

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
