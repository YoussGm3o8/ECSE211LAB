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
    print("Drum system running.")
    
    try:
        # Start the motor
        start_motor()

    except KeyboardInterrupt:
        print("Program interrupted by user.")
        stop_motor()  # Ensure motor is stopped when exiting
