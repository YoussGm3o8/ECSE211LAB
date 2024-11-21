import components.navigation as nav
from components.navigation import SLOW, MODERATE, FAST
from components.engine import start, end, global_state, get_state
import time


#I don't know why we would need threading or if its advantageous to use it in this case
def avoid_water_using_threads():
    try:
        start()
        while True:
            state = global_state.get()
            if state.color_sensor == "b" or state.color_sensor == "p":
                nav.turn(SLOW)
                print("right")
            elif state.color_sensor2 == "b" or state.color_sensor2 == "p":
                nav.turn(-SLOW)
                print("left")
            else:
                nav.forward(MODERATE)
                print("forward")
    finally:
        end()

def avoid_water_without_threads():
    ENABLES = [True, True, True, True]
    try:
        while True:
            state = get_state(ENABLES)
            print(state.color_sensor)
            print(state.color_sensor2)
            if state.color_sensor == "unkown" or state.color_sensor2 == "unkown":
                nav.stop()
                time.sleep(0.1)
            if state.color_sensor == "b" or state.color_sensor == "p":
                nav.turn(-SLOW)
                print("right")
            elif state.color_sensor2 == "b" or state.color_sensor2 == "p":
                nav.turn(SLOW)
                print("left")
            else:
                return True
                #nav.forward(MODERATE)
                #print("forward")

            time.sleep(0.05)
    finally:
        end()


if __name__ == "__main__":
    avoid_water()
