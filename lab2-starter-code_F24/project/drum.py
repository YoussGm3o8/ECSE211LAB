from button_manager import ButtonManager
from utils.brick import Motor
import time

# Initialize motor on port A
motor = Motor("A")

# Global variable for motor speed in degrees per second
motor_speed_dps = 360  # Adjust as needed

# Function to start the motor at the specified speed
def start_motor():
    print("Starting the motor.")
    motor.set_dps(motor_speed_dps)  # Start the motor at the specified speed

# Function to stop the motor
def stop_motor():
    print("Stopping the motor.")
    motor.set_dps(0)  # Stop the motor

# Example usage
if __name__ == "__main__":
    print("Drum system running with Button Manager.")

    # Create an instance of ButtonManager
    button_manager = ButtonManager()

    # Map buttons to motor functions
    # Button 4 press will start the motor
    button_manager.add_callback(start_motor, 4)  # 4 => Button 1 (1000)
    # Button 1,2,3,4 press will stop the motor
    button_manager.add_callback(stop_motor, 15)   # 15 => Button 1,2,3,4 (1111)

    try:
        while True:
            button_manager.update()  # Continuously check for button presses
            sleep(0.1)  # Small delay to avoid excessive CPU usage

    except KeyboardInterrupt:
        print("Program stopped by user.")
        stop_motor()  # Safely stop the motor when exiting
