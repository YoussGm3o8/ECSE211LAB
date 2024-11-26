import components.engine as engine
from common.filters import Delta, Diff
import components.navigation as nav
import time
from communication.client import Client
from collections import namedtuple


FSM_state = namedtuple("FSM_state", ["state", "arguments"])

def forward_listen(FSM, args):
    print("forward_listen")
    nav.forward(nav.SLOW)
    memory = None
    last = None
    while True:
        state = engine.get_state()
        if state.us_sensor is None:
            continue #may be problematic (no sleep)

        if state.us_sensor < 10:
            return FSM_state("near_object", None)
        if last is None:
            last = state.us_sensor
            continue
        val = FSM.delt.get(state.us_sensor)

        if val > 10:
            return FSM_state("refocus", val)
        time.sleep(0.05)
        if FSM.client is not None:
            FSM.client.send(FSM_state("forward_listen", state.us_sensor))

def near_object(FSM, args):
    print("near_object")
    return FSM_state("end", None)

def follow_gradient_ranged(treshold=40, client_callback=None):
    """
    The car is supposed to rotate until it detects a cube and oscillate around it
    """
    d = Diff(3, 1.5, 0.8)
    speed = 150
    nav.turn(speed)
    ti = time.time()
    state = engine.get_state()
    while True:
        # if time.time() - ti > 5:
        #     print("couldnt locate object")
        #     nav.turn(-speed)
        #     time.sleep(5)
        #     nav.stop()
        #     return None
        state = engine.get_state()
        if state.us_sensor is None:
            continue
        if state.g_sensor is None:
            continue
        t = time.time()
        us_v = state.us_sensor if state.us_sensor < treshold else treshold
        val = d.update(t, us_v)
        if val:
            dist = d.down[-1][0]
            print(dist)
            nav.turn(-speed)
            while (dist - 3 < state.us_sensor < dist + 3):
                continue
            nav.stop()
            return

        time.sleep(0.05)
        if FSM.client is not None:
            FSM.client.send(FSM_state("refocus", us_v))


def refocus_v2(FSM, args):
    follow_gradient_ranged()
    return FSM_state("forward_listen", None)


def refocus(FSM, args):
    print("refocus")
    speed = nav.SLOW
    nav.turn(speed)
    while True:
        state = engine.get_state()
        if state.us_sensor is None:
            continue
        val = FSM.delt.get(state.us_sensor)

        if val < -10:
            return FSM_state("forward_listen", None)

        if FSM.client is not None:
            FSM.client.send(FSM_state("refocus", state.us_sensor))

        time.sleep(0.05)

class FiniteStateMachine:
    def __init__(self, initial_state, states={
        "forward_listen": forward_listen,
        "end": None,
        "near_object": near_object,
        "refocus": refocus
    }):
        self.delt = Delta()
        self.client = Client()
        self.goal = None
        self.states_dict = states
        self.current = FSM_state(initial_state, None)

    def start(self):
        print("start")
        while True:
            if self.current.state == "end":
                break
            self.current = self.states_dict[self.current.state](self, self.current.arguments) #may want to use get() instead of []


    def end(self, *args):
        print("end")
        engine.end()

if __name__ == "__main__":
    FSM = FiniteStateMachine("forward_listen")
    #initialize the components
    try:
        FSM.start()
    finally:
        FSM.end()
        FSM.client.exit()