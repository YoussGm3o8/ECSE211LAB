import components.navigation as nav
import statistics as stat
import components.engine as engine
from common.filters import Diff, Deriver, Exponential_Moving_Average, Convolution, SquareWave
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
    """
    The car is supposed to rotate until it detects a cube and oscillate around it
    """
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

def follow_gradient_v2(client_callback=None):
    """
    The car is supposed to rotate until it detects a cube and oscillate around it

    THIS IS BY FAR THE BEST IMPLEMENTATION HOWEVER IT MAY BE TOO SENSITIVE TO NOISE
    """
    try:
        de = Deriver(4)
        ema = Exponential_Moving_Average(0.05)
        speed = nav.SLOW
        state = engine.get_state()
        while state.raw_us_sensor is None:
            state = engine.get_state()
        ema.reset(state.raw_us_sensor)
        nav.turn(speed)
        while True:
            time.sleep(0.05)
            state = engine.get_state()
            if state.raw_us_sensor is None:
                continue
            mean = ema.update(state.raw_us_sensor)
            val = de.update(mean) if state.raw_us_sensor > mean else de.update(state.raw_us_sensor)

            if val < 0:
                speed *= -1
                nav.turn(speed)

            if client_callback is not None:
                client_callback(("nav", (state.raw_us_sensor, val)))
    finally:
        engine.end()

def follow_signals(client_callback=None):
    """
    The car is supposed to rotate until it detects a cube and oscillate around it

    NOTE: the us_sensor must not be median_filtered
    """
    try:
        treshold = 2.5
        kernel = SquareWave(6) #we may want to change this to a greater value if we want to detect cubes from closer distances
        conv = Convolution(kernel)
        ema = Exponential_Moving_Average(0.05)
        state = engine.get_state()
        while state.raw_us_sensor is None:
            state = engine.get_state()
            time.sleep(0.05)
        ema.reset(state.raw_us_sensor)
        speed = nav.SLOW
        nav.turn(speed)
        while True:
            time.sleep(0.05)
            state = engine.get_state()
            if state.raw_us_sensor is None:
                continue
            mean = ema.update(state.raw_us_sensor)
            val = conv.update(mean) if state.raw_us_sensor > mean else conv.update(state.raw_us_sensor)

            if val < -treshold:
                speed *= -1
                nav.turn(speed)

            if client_callback is not None:
                client_callback(("nav", (state.raw_us_sensor, val)))
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

        Adds a memory element to get closer to the cube blindly
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
