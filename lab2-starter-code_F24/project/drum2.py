from threading import Thread
import time

drum_flag = False
not_exit = True

def drumstart():
    global drum_flag
    drum_flag = True

def drumstop():
    global drum_flag
    drum_flag = False

def exit():
    #Always call this to close the drum thread
    global not_exit
    not_exit = False
    th.join()

def drumloop():
    while not_exit:
        if drum_flag:
            pass
        time.sleep(0.1)

th = Thread(target=drumloop)
th.start()


