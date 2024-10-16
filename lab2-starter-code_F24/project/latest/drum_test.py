from utils.brick import Motor, wait_ready_sensors, TouchSensor
import time
TOUCH_SENSOR1 = TouchSensor(3)
TOUCH_SENSOR2 = TouchSensor(4)
wait_ready_sensors()
motor = Motor(port="B")

def play_drum():
    motor.set_power(50)
    while True:
        time.sleep(0.33)
        motor.set_position_relative(-180)
if __name__=='__main__':
    play_drum()
    
    