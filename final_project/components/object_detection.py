import components.navigation as nav
import engine
from common.filters import Median_Filter, EMA, EMA_Derivatives
import time


def scan_mean(client_callback=None):
    nav.turn(nav.MODERATE)
    state = engine.get_state()
    mean = state.g_sensor
    for _ in range(30):
        if client_callback is not None:
            client_callback(("mean", state.g_sensor))
        time.sleep(0.05)
        state = engine.get_state()
        mean += state.g_sensor
    nav.stop()
    return mean / 31

def scan_back(mean, treshold=10, client_callback=None):
    avg = EMA(alpha=0.05)
    avg.reset(mean)
    med = Median_Filter(10)

    nav.turn(-nav.MODERATE)
    state = engine.get_state()
    ema = EMA_Derivatives((state.g_sensor,state.us_sensor), alpha=0.55)
    med.update(state.us_sensor)
    d1 = None

    while True:
        time.sleep(0.05)
        state = engine.get_state()
        m = med.update(state.us_sensor)
        a = avg.update(state.us_sensor)

        d0 = ema.update((state.g_sensor, state.us_sensor))

        if d1 is None:
            d1 = d0
            continue

        if d1 * d0 < 0:
            if m < a - treshold:
                nav.stop()
                return state.g_sensor
            else:
                print("possible signal detected here (change treshold if this is false negative)")
        elif abs(d0) < 0.01:
            if m < a - treshold:
                nav.stop()
                return state.g_sensor
            else:
                print("possible signal detected here (change treshold if this is false negative)")

        if client_callback is not None:
            client_callback(("scan", (m, a, d0, d1, treshold)))
