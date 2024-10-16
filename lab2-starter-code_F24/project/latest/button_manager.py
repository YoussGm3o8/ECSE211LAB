#!/usr/bin/env python3

from utils.brick import TouchSensor, wait_ready_sensors

class ButtonManager:
    """ 
    A class to manage the buttons on the robot see debug/buttons_manager_ex.py for an example of how to use it
    """

    def __init__(self):
        self.callbacks = {}
        self.TOUCH_SENSOR1 = TouchSensor(1)
        self.TOUCH_SENSOR2 = TouchSensor(2)
        self.TOUCH_SENSOR3 = TouchSensor(3)
        self.TOUCH_SENSOR4 = TouchSensor(4)
        #self.prev = -1
        wait_ready_sensors()  # Note: Touch sensors actually have no initialization time

    def add_callback(self, callback, id: int):
        """
        Add a callback to a button combination

        Parameters
            callback: function to be called when the button is pressed
            id: is a number between 0 and 15 that represents the combination of the buttons (i.e. 3 => 0011)
        """

        self.callbacks[id] = callback

    def update(self):
        """
        use this in a loop to call the callbacks when the buttons are pressed

        Returns:
            bool: True if a callback was called, False otherwise
        """

        cid = 0
        if self.TOUCH_SENSOR1.is_pressed():
            cid += 1
        if self.TOUCH_SENSOR2.is_pressed():
            cid += 2
        if self.TOUCH_SENSOR3.is_pressed():
            cid += 4
        if self.TOUCH_SENSOR4.is_pressed():
            cid += 8

        # comment this if you must
        #if self.prev == cid:
         #   return False 
#         self.prev = cid

        ret = self.callbacks.get(cid)

        if ret is not None:
            ret()
            return True
        else:
            return False

