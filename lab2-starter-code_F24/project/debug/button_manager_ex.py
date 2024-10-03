#ignore this file, it is not used in the project.
#bottom of file for the example
import pygame
import time


def wait_ready_sensors():
    pass

simulated_touch_sensor = [False]*4
flags = [False]


def simulate_buttons():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                simulated_touch_sensor[0] = True
            if event.key == pygame.K_2:
                simulated_touch_sensor[1] = True
            if event.key == pygame.K_3:
                simulated_touch_sensor[2] = True
            if event.key == pygame.K_4:
                simulated_touch_sensor[3] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_1:
                simulated_touch_sensor[0] = False
            if event.key == pygame.K_2:
                simulated_touch_sensor[1] = False
            if event.key == pygame.K_3:
                simulated_touch_sensor[2] = False
            if event.key == pygame.K_4:
                simulated_touch_sensor[3] = False
            if event.key == pygame.K_q:
                print("exiting...")
                flags[0] = True
class TouchSensor:
    def __init__(self, port: int):
        self.port = port

    def is_pressed(self):
        return simulated_touch_sensor[self.port-1]


class ButtonManager:
    def __init__(self):
        self.callbacks = {}
        self.TOUCH_SENSOR1 = TouchSensor(1)
        self.TOUCH_SENSOR2 = TouchSensor(2)
        self.TOUCH_SENSOR3 = TouchSensor(3)
        self.TOUCH_SENSOR4 = TouchSensor(4)
        self.prev = -1
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
        if self.prev == cid:
            return False 
        self.prev = cid

        ret = self.callbacks.get(cid)

        if ret is not None:
            ret()
            return True
        else:
            return False

if __name__ == "__main__":
    """
        Example usage of ButtonSystem
    """

    pygame.init()
    pygame.display.set_mode((100, 100))

    #create the class to init the buttons inputs
    bm = ButtonManager()

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
    bm.add_callback(lambda: print("8"), 8)
    bm.add_callback(lambda: print("9"), 9)
    bm.add_callback(lambda: print("10"), 10)
    bm.add_callback(lambda: print("11"), 11)
    bm.add_callback(lambda: print("12"), 12)
    bm.add_callback(lambda: print("13"), 13)
    bm.add_callback(lambda: print("14"), 14)
    bm.add_callback(lambda: print("15"), 15)

    #main loop
    while(not flags[0]):
        #ignore this
        simulate_buttons()

        #this is the important part
        #bm.update() will call the appropriate callback when the buttons are pressed
        bm.update()
        time.sleep(0.05)

    pygame.quit()


