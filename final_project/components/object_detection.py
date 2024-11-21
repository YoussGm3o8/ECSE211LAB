import components.navigation as nav
import components.engine as engine
from common.filters import diff, Deriver
import time
import communication.client as client


def scan(maxtime=None, client_callback=None):
    """
    Turn until a bloc is detected
    """
    d = diff(2.5, 20, 0.7) #ideally we change these parameters for each distances (close, medium, far)
    d2 = diff(5, 50, 1) #ideally we change these parameters for each distances (close, medium, far)
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

def navigate_row(client_callback=None):
    d = Deriver(8)
    try:
        while True:
            time.sleep(0.05)
            state = engine.get_state()
            if state.us_sensor is None:
                continue
            val = d.update(state.us_sensor)
            if val is None:
                continue
            if val < 0 and state.us_sensor < 30:
                nav.turn(-nav.SLOW)
            elif val > 0:
                nav.turn(nav.SLOW)
            if client_callback is not None:
                client_callback(("nav", (state.us_sensor, val)))
    finally:
        engine.end()

def run_row(client_callback=None):
    try:
        nav.forward(nav.SLOW)
        while True:
            time.sleep(0.05)
            state = engine.get_state()
            if client_callback is not None:
                client_callback(("row", state))
    finally:
        engine.end()
