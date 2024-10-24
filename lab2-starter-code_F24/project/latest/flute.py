import utils.sound as sound  # Import the sound module from utils

class player:
    def __init__(self, cutoff):
        """
        Initialize the player object with a sound object (flute) and predefined musical notes.
        
        Parameters:
        cutoff (float/int): The cutoff frequency for the sound object.
        """
        # Initialize the flute sound with a duration of 0.21 seconds and full volume (100).
        self.flute = sound.Sound(duration=0.21, volume=100)
        self.flute.set_cutoff(cutoff)  # Set the cutoff frequency for the flute.
        self.flute.update_audio(True)  # Enable audio updates for the flute.

        # Define a dictionary of musical notes and their corresponding frequencies (in Hz).
        self.notes = {
            "BG": 0,        # Background or silence
            "C1": 261.63,
            "D1": 293.66,
            "E1": 329.63,
            "F1": 349.23,
            "G1": 392.00,
            "A1": 440.00,
            "B1": 493.88,
            "C2": 523.25,
            "D2": 587.33,
            "E2": 659.25,
            "F2": 698.46,
            "G2": 783.99,
            "A2": 880.00,
            "B2": 987.77,
            "C3": 1046.50,
            "D3": 1174.66,
            "E3": 1318.51,
            "F3": 1396.91,
            "G3": 1567.98,
            "A3": 1760.00,
            "B3": 1975.53,
        }

    def play(self, note):
        """
        Play the specified musical note.
        
        Parameters:
        note (str): The note to be played (e.g., 'C1', 'D2').
        """
        pitch = self.notes[note]  # Get the pitch (frequency) of the note from the dictionary.
        # Create a new Sound object with a slightly longer duration (0.22 seconds) and the given pitch.
        self.flute = sound.Sound(duration=0.22, pitch=pitch, volume=100)
        self.flute.update_audio(True)  # Enable audio updates for the new sound object.
        self.flute.play()  # Play the sound.

    def stop(self):
        """Stop the sound and reset the audio settings."""
        self.flute.stop()  # Stop the currently playing sound.
        self.flute.reset_audio()  # Reset the audio system to its initial state.

    def update(self):
        """Update the duration of the flute sound."""
        self.flute.update_duration(0.1)  # Update the sound's duration to 0.1 seconds.
