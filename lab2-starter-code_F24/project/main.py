from drum import Drum
import flute
from button_manager import ButtonManager
from playsound import playsound
import time
import os

def kick():
    playsound(path)

if __name__ == "__main__":
    path = os.path.join("debug", "kick.wav")
    dm = Drum(kick, 0.33)
    bm = ButtonManager()
    fl = flute.player()

    bm.add_callback(lambda: fl.play("C1"), 1)
    bm.add_callback(lambda: fl.play("D1"), 2)
    bm.add_callback(lambda: fl.play("E1"), 4)
    bm.add_callback(lambda: fl.play("F1"), 3)
    bm.add_callback(lambda: fl.play("G1"), 6)
    bm.add_callback(lambda: fl.play("A1"), 7)
    bm.add_callback(lambda: fl.play("B1"), 9)
    bm.add_callback(dm.mute, 8)
    bm.add_callback(dm.play, 15)

    try:
        while True:
            bm.update()  # Continuously check for button presses
            time.sleep(0.1)  # Small delay to avoid excessive CPU usage

    except KeyboardInterrupt:
        print("Program stopped by user.")

    finally:
        dm.exit() #Safely exit drum thread
