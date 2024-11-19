import time

def poll(func, *arg):
    """
    arg1: function to poll
    *arg : arguments for the function
    """

    while True:
        val = func(*arg)
        if val is not None:
            return val

def poll_with_timeout(timeout, func, *arg):
    """
    same as poll but times out after arg: timeout
    """
    ti = time.time()
    while True:
        val = func(*arg)
        if val is not None:
            return val
        if time.time() - ti > 5:
            return
