from threading import Thread  # Import the Thread class for concurrent execution
import time  # Import the time module to manage sleep intervals

class Drum:
    def __init__(self, callback, sleep_time=1):
        """
        Initialize the Drum object.
        
        Parameters:
        callback (function): A function to be called when the drum is 'played'.
        sleep_time (int/float): The time interval (in seconds) between successive 'drum beats'.
        """
        self.drum_flag = False  # Flag to indicate whether the drum is active (playing).
        self.not_exit = True  # Flag to control when to exit the drum thread.
        self.func = callback  # Assign the callback function to be triggered on drum play.
        self.sleep_time = sleep_time  # Set the sleep interval between beats.

        # Create a thread that runs the drumloop method and start the thread.
        self.th = Thread(target=self.drumloop)
        self.th.start()

    def play(self):
        """Activate the drum to start playing (set the drum flag to True)."""
        self.drum_flag = True

    def mute(self):
        """Mute the drum to stop playing (set the drum flag to False)."""
        self.drum_flag = False

    def exit(self):
        """Stop the drum thread gracefully by updating the not_exit flag and joining the thread."""
        self.not_exit = False  # Set flag to False to stop the drumloop.
        self.th.join()  # Wait for the drum thread to complete before continuing.

    def drumloop(self):
        """
        The main loop of the drum, executed in a separate thread.
        Continuously checks if the drum should play and triggers the callback function.
        """
        while self.not_exit:  # Keep running the loop until the drum is exited.
            if self.drum_flag:  # If drum is active, call the callback function.
                self.func()
            time.sleep(self.sleep_time)  # Sleep for the specified interval before the next loop iteration.
