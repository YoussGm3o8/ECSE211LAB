import utils.sound as sound

class player:
    def __init__(self, cutoff):
        self.flute = sound.Sound(duration=0.21, volume=100)
        self.flute.set_cutoff(cutoff)
        self.flute.update_audio(True)
        

        self.notes = {
                "BG": 0,
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
        pitch = self.notes[note]
        self.flute = sound.Sound(duration=0.22, pitch = pitch, volume=100)
        self.flute.update_audio(True)
        self.flute.play()

    def stop(self):
        self.flute.stop()
        self.flute.reset_audio()
        
    def update(self):
        self.flute.update_duration(0.1)
