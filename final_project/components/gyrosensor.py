from utils.brick import EV3GyroSensor

#WARNING: Do not handle None values here. Handle this in the robot logic loop
class GYRO_Sensor(EV3GyroSensor):
    def __init__(self, port):
        super().__init__(port)
        print(f"waiting for gyro on port {port}")
        self.set_mode(self.Mode.ABS)
        self.wait_ready()

    def __str__(self):
        return f"GYRO_Sensor(port={self.port})"

    def fetch(self):
        return self.get_value()
    
    def reset(self):
        self.reset_measure()