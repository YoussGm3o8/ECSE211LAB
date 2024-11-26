import components.navigation as nav
import statistics as stat
import components.engine as engine
from common.filters import Diff, Deriver
import time
import communication.client as client


def scan(maxtime=None, client_callback=None):
    """
    Turn until a bloc is detected
    """
    d = Diff(2.5, 20, 0.7) #ideally we change these parameters for each distances (close, medium, far)
    d2 = Diff(5, 50, 1) #ideally we change these parameters for each distances (close, medium, far)
    nav.turn(nav.SLOW)

    if maxtime is not None:
        iterations = int(maxtime / 0.05)
    else:
        iterations = 100000
    for _ in range(iterations):
        state = engine.get_state()
        if d2.update(state.g_sensor, state.us_sensor):
            nav.stop()
            return d2.down[-1]
        if d.update(state.g_sensor, state.us_sensor):
            nav.stop()
            return d.down[-1] #alternatively you can return the midpoint between d.up[-1][0] and d.down[-1][0]
        if client_callback is not None:
            client_callback(("scan", (state.g_sensor, state.us_sensor, d.up, d.down, d.treshold, d.width)))
        time.sleep(0.05)
    nav.stop()
    return None

# def follow_gradient(client_callback=None):
#     d = Deriver(8)
#     try:
#         while True:
#             time.sleep(0.05)
#             state = engine.get_state()
#             if state.us_sensor is None:
#                 continue
#             val = d.update(state.us_sensor)
#             if val is None:
#                 continue
#             if val < 0 and state.us_sensor < 30:
#                 nav.turn(-nav.SLOW)
#             elif val > 0:
#                 nav.turn(nav.SLOW)
#             if client_callback is not None:
#                 client_callback(("nav", (state.us_sensor, val)))
#     finally:
#         engine.end()

def follow_gradient(client_callback=None):
    try:
        d = Diff(6, 1.5, 0.8)
        speed = nav.SLOW
        nav.turn(speed)
        while True:
            time.sleep(0.05)
            state = engine.get_state()
            if state.us_sensor is None:
                continue
            val = d.update(time.time(), state.us_sensor)

            if val:
                speed *= -1
                nav.turn(speed)

            if client_callback is not None:
                client_callback(("nav", (state.us_sensor, val)))
    finally:
        engine.end()

def run_row(client_callback=None):
    try:

        """
        move forward in a row until a jump in signal is detected (a cube is outside of range)
        """
        nav.forward(nav.SLOW)
        de = Deriver(5)
        jump_size = None
        end = False
        while True:
            time.sleep(0.05)
            state = engine.get_state()
            if state.us_sensor is None:
                continue
            if state.us_sensor < 5:
                nav.stop()
                end = True
                break

            val = de.update(state.us_sensor)
            if val is None:
                continue
            if val > 0:
                jump_size = val
                nav.stop()
                break

            if client_callback is not None:
                client_callback(("row", state))

        if end:
            print("sucess!")
            return


        if jump_size is None:
            print("error jump_size is None which is impossible")
            return

        d = Diff(int(jump_size*0.6), 1.5, 0.8)

        speed = -nav.SLOW
        nav.turn(speed)
        while True:
            time.sleep(0.05)
            state = engine.get_state()
            if state.us_sensor is None:
                continue
            val = d.update(time.time(), state.us_sensor)

            if val:
                speed *= -1
                nav.turn(speed)
            if client_callback is not None:
                client_callback(("row", state))
    finally:
        engine.end()


def run_row_v2(client_callback=None):
    try:

        """
        move forward in a row until a jump in signal is detected (a cube is outside of range)
        """
        nav.forward(nav.SLOW)
        diff_tracker = Deriver(5)
        memory = None
        jump_size = 10

        while True:
            state = engine.get_state()
            if state.us_sensor is None:
                continue
            d = diff_tracker.update(state.us_sensor, False)

            if d is None:
                continue

            if memory is not None:
                memory += d
                if memory <= 20:
                    nav.stop()
                    break

            if d > diff_tracker.treshold:
                jump_size = d
                if len(diff_tracker.values) >= 5:
                    memory = stat.median(diff_tracker.values[-6:-1])
                else:
                    memory = stat.median(diff_tracker.values)

            elif d < -diff_tracker.treshold:
                jump_size = 10
                memory = None

            if state.us_sensor < 10:
                nav.stop()
                break

            if client_callback is not None:
                client_callback(("row", state))

            time.sleep(0.05)

        #rotate until detecting the object
        d = Diff(int(jump_size*0.7), 1.5, 0.8)

        speed = -nav.SLOW
        nav.turn(speed)
        while True:
            state = engine.get_state()
            if state.us_sensor is None:
                continue
            val = d.update(time.time(), state.us_sensor)

            if val:
                speed *= -1
                nav.turn(speed)
            if client_callback is not None:
                client_callback(("row", state))
            time.sleep(0.05)

    finally:
        engine.end()
