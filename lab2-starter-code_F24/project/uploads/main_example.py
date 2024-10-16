from drum import Drum
import debug.button_manager_ex as bme
import pygame
from playsound import playsound
import time
import os

path = os.path.join("debug", "kick.wav")

def kick():
    playsound(path)

if __name__ == "__main__":
    
    dm = Drum(kick, 0.33)

    pygame.init()
    pygame.display.set_mode((100, 100))

    #create the class to init the buttons inputs
    bm = bme.ButtonManager()

    #add your callbacks (functions to play sounds, etc)
    #see the documention in add_callback for arguments
    bm.add_callback(lambda: print("0"), 0)
    bm.add_callback(lambda: print("1"), 1)
    bm.add_callback(lambda: print("2"), 2)
    bm.add_callback(lambda: print("3"), 3)
    bm.add_callback(lambda: print("4"), 4)
    bm.add_callback(lambda: print("5"), 5)
    bm.add_callback(lambda: print("6"), 6)
    bm.add_callback(lambda: print("7"), 7)
    bm.add_callback(dm.mute, 8)
    bm.add_callback(lambda: print("9"), 9)
    bm.add_callback(lambda: print("10"), 10)
    bm.add_callback(lambda: print("11"), 11)
    bm.add_callback(lambda: print("12"), 12)
    bm.add_callback(lambda: print("13"), 13)
    bm.add_callback(lambda: print("14"), 14)
    bm.add_callback(dm.play, 15)

    #main loop
    while(not bme.flags[0]):
        #ignore this
        bme.simulate_buttons()

        #this is the important part
        #bm.update() will call the appropriate callback when the buttons are pressed
        bm.update()
        time.sleep(0.05)

    dm.exit() #exit drum when done

    pygame.quit()
