from drum import Drum  # Import the Drum class
import flute  # Import the flute module
from utils import sound  # Import sound utilities
from button_manager import ButtonManager  # Import the ButtonManager for handling button inputs
from utils.brick import Motor  # Import Motor to control a motor
import time  # Import time module for delays

# Global flag to indicate when the program should exit
exit_flag = True
# Initialize a Motor object on port "B"
motor = Motor("B")
i = 0  # Counter for tracking the number of times the kick function is called

def kick():
    """
    Function to simulate a kick drum sound and control the motor's movement.
    """
    global i
    print(i)  # Print the current value of i (for debugging purposes)
    i += 1  # Increment the counter each time the kick function is called
    motor.set_dps(360)  # Set the motor's speed in degrees per second
    motor.set_position_relative(180)  # Move the motor by 180 degrees

def safe_exit():
    """
    Function to safely exit the program by setting the exit_flag to False.
    """
    global exit_flag
    exit_flag = False  # This will stop the main loop

if __name__ == "__main__":
    # Initialize a Drum object with the kick function and a 0.1 second interval
    dm = Drum(kick, 0.1)
    # Initialize the ButtonManager to handle button inputs
    bm = ButtonManager()
    # Initialize the flute player with a cutoff frequency of 0.5
    fl = flute.player(0.5)

    # Add callbacks to play different flute notes
    bm.add_callback(lambda: fl.play("C1"), 1)
    bm.add_callback(lambda: fl.play("D1"), 2)
    bm.add_callback(lambda: fl.play("E1"), 3)
    bm.add_callback(lambda: fl.play("F1"), 4)
    bm.add_callback(lambda: fl.play("G1"), 5)
    bm.add_callback(lambda: fl.play("A1"), 6)
    bm.add_callback(lambda: fl.play("B1"), 7)

    # Add callbacks to control the drum: Button 8 starts the drum, Button 9 emergency stops
    bm.add_callback(dm.mute, 9)  # Emergency Stop
    bm.add_callback(dm.play, 8)  # Start  the drum

    bm.add_callback(safe_exit, 15) #  Safe exit.

    try:
        # Main loop to check button states and update the ButtonManager
        while exit_flag:
            bm.update()  # Continuously check for button presses
            time.sleep(0.07)  # Delay to prevent high CPU usage

    except KeyboardInterrupt:
        # If the user presses Ctrl+C, exit the program
        print("Program stopped by user.")

    finally:
        # Cleanup actions before exiting
        print("exiting...")
        dm.exit()  # Safely stop the drum thread
        motor.set_dps(0)  # Stop the motor
        exit()  # Exit the program
