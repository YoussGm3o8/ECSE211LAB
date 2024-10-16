from drum import Drum
import flute
from utils import sound
from button_manager import ButtonManager
from utils.brick import Motor
import time
exit_flag = True
motor = Motor("B")
i = 0 
def kick():
    global i
    print(i)
    i += 1
    motor.set_dps(360)
    motor.set_position_relative(180)
    #motor.set_power(50)

def safe_exit():
    global exit_flag
    exit_flag = False

if __name__ == "__main__":
    dm = Drum(kick, 0.1)
    bm = ButtonManager()
    fl = flute.player(0.5) #cutoff

    bm.add_callback(lambda: fl.play("C1"), 1)
    bm.add_callback(lambda: fl.play("D1"), 2)
    bm.add_callback(lambda: fl.play("E1"), 3)
    bm.add_callback(lambda: fl.play("F1"), 4)
    bm.add_callback(lambda: fl.play("G1"), 5)
    bm.add_callback(lambda: fl.play("A1"), 6)
    bm.add_callback(lambda: fl.play("B1"), 7)
    bm.add_callback(dm.mute, 9)
    bm.add_callback(dm.play, 8)
    bm.add_callback(safe_exit, 15)

    try:
        while exit_flag:
            bm.update()  # Continuously check for button presses
            time.sleep(0.07)  # Small delay to avoid excessive CPU usage

    except KeyboardInterrupt:
        print("Program stopped by user.")

    finally:
        print("exiting...")
        dm.exit() #Safely exit drum thread
        motor.set_dps(0)
        exit()
        
