import threading

RUNNING_THREADS = []

class ThreadEngine:
    def __init__(self):
        self.threads = []

    def loop(self, func, *args):
        assert(callable(func))
        id = len(self.threads)
        RUNNING_THREADS.append(True)
        self.threads.append(threading.Thread(target=self.start, args=(func, id, *args)))
        self.threads[id].start()
        return id

    @staticmethod
    def start(func, id, *args):
        while RUNNING_THREADS[id]:
            func(*args)

    def join(self, id):
        RUNNING_THREADS[id] = False
        self.threads[id].join()

    def join_all(self):
        for i in range(len(RUNNING_THREADS)):
            RUNNING_THREADS[i] = False
        for t in self.threads:
            t.join()

if __name__ == "__main__":
    engine = ThreadEngine()
    engine.loop(print, "Hello, World!")
    engine.join_all()
