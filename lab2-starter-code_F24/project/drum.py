from threading import Thread
import time

class Drum:

    def __init__(self,callback, sleep_time=0.1):
        self.drum_flag = False
        self.not_exit = True
        self.func = callback
        self.sleep_time = sleep_time

        self.th = Thread(target=self.drumloop)
        self.th.start()

    def play(self):
        self.drum_flag = True

    def mute(self):
        self.drum_flag = False

    def exit(self):
        #Always call this to close the drum thread
        self.not_exit = False
        self.th.join()

    def drumloop(self):
        while self.not_exit:
            if self.drum_flag:
                self.func()
            time.sleep(self.sleep_time)
