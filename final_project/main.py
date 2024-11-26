import components.engine as engine
from common.filters import Delta
from components.navigation import nav
import time
from communication.client import Client
from collections import namedtuple


FSM_state = namedtuple("FSM_state", ["state", "arguments"])

def forward_listen(FSM, args):
    print("forward_listen")
    nav.forward(nav.SLOW)
    while True:
        state = engine.get_state()

        if state.us_sensor is None:
            continue #may be problematic (no sleep)

        if state.us_sensor < 5:
            return FSM_state("near_object", None)

        val = FSM.delt.get(state.us_sensor)

        if val > 5:
            return FSM_state("refocus", val)
        time.sleep(0.05)
        if FSM.client is not None:
            FSM.client.send(FSM_state("forward_listen", state))

def near_object(FSM, args):
    print("near_object")
    return FSM_state("end", None)

def refocus(FSM, args):
    print("refocus")
    speed = -nav.SLOW
    nav.turn(speed)
    while True:
        state = engine.get_state()
        if state.us_sensor is None:
            continue
        val = FSM.delt.get(state.us_sensor)

        if val < -5:
            return FSM_state("forward_listen", None)

        if FSM.client is not None:
            FSM.client.send(FSM_state("refocus", state))

        time.sleep(0.05)

class FiniteStateMachine:
    def __init__(self, initial_state, states={
        "forward_listen": forward_listen,
        "end": None,
        "near_object": near_object,
        "refocus": refocus
    }):
        self.goal = None
        self.states_dict = states
        self.current = FSM_state(initial_state, None)

    def start(self):
        print("start")
        while True:
            if self.current.state == "end":
                break
            self.current = self.states_dict[self.current.state](self, self.current.arguments) #may want to use get() instead of []


    def end():
        print("end")
        engine.end()

if __name__ == "__main__":
    FSM = FiniteStateMachine()
    #initialize the components
    FSM.delt = Delta()
    FSM.client = Client()
    try:
        FSM.start()
    finally:
        FSM.end()
        FSM.client.exit()

