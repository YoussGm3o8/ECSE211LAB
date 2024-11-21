"""
wall_follower.py

DESCRIPTION: A robot that follows walls using an ultrasonic sensor and EV3 motors
"""
import time
from components.gyrosensor import g_sensor
import components.navigation as nav
from components.ultrasonic import us_sensor

# CONSTANTS
DESIRED_DISTANCE = 20  # Desired distance from the wall (cm)
KP = 1.0               # Proportional control constant
BASE_SPEED = 180       # Base motor speed (degrees per second)
TIMEOUT = 10           # Timeout for sensor functions

# Helper function: Timeout for sensor readings
def wait_for(func, *args):
    if not callable(func):
        raise TypeError("func must be a function")
    ti = time.time()
    v = func(*args)
    while v is None:
        v = func(*args)
        if time.time() - ti > TIMEOUT:
            if hasattr(func, "__self__"):
                # Debugging info
                myclass = func.__self__
                raise TimeoutError(str(myclass) + " not responding...")
            raise TimeoutError("Component not responding...")
    return v

# Wall-following logic
def wall_follow():
    try:
        while True:
            # Fetch distance from the ultrasonic sensor
            distance = us_sensor.fetch()
            if distance is None:
                print("Ultrasonic sensor error; retrying...")
                distance = wait_for(us_sensor.fetch)

            # Calculate error and turn adjustment using proportional control
            error = DESIRED_DISTANCE - distance
            turn_speed = KP * error

            # Adjust motor speeds based on distance to the wall
            left_speed = BASE_SPEED + turn_speed
            right_speed = BASE_SPEED - turn_speed

            # Navigate using the adjusted speeds
            nav.set_speed(left_speed, right_speed)

            # Debugging info
            print(f"Distance: {distance} cm | Error: {error:.2f} | Speeds: L={left_speed}, R={right_speed}")
            time.sleep(0.05)  # Small delay to stabilize loop

    except KeyboardInterrupt:
        # Gracefully stop the robot on Ctrl+C
        nav.stop()
        print("Wall-following stopped.")

# MAIN FUNCTION
def main():
    try:
        print("Starting wall-following...")
        wall_follow()
    finally:
        nav.stop()
        print("Program terminated.")

if __name__ == "__main__":
    main()
