import threading



global RUNNING_THREADS
RUNNING_THREADS = []

class ThreadEngine:
    def __init__(self):
        self.threads = []

    def loop(self, func, args):
        assert(callable(func))
        id = len(self.threads)
        RUNNING_THREADS.append(True)
        self.threads.append(threading.Thread(target=self.start(func, args, id), args=args))
        self.threads[id].start()
    
    @staticmethod
    def start(func, args, id):
        while RUNNING_THREADS[id]:
            func(*args)


    def join_all(self):

        for i in range(len(RUNNING_THREADS)):
            RUNNING_THREADS[i] = False

        for t in self.threads:
            t.join()

