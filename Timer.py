import threading
#from threading import Thread
def Timer(*args, **kwargs):
    """Factory function to create a Timer object.

    Timers call a function after a specified number of seconds:

        t = Timer(30.0, f, args=[], kwargs={})
        t.start()
        t.cancel()     # stop the timer's action if it's still waiting

    """
    return _Timer(*args, **kwargs)

class _Timer(threading.Thread):
    """Call a function after a specified number of seconds:

            t = Timer(30.0, f, args=[], kwargs={})
            t.start()
            t.cancel()     # stop the timer's action if it's still waiting

    """

    def __init__(self, interval, function, args=[], kwargs={}):
        threading.Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = threading.Event()

    def cancel(self):
        """Stop the timer if it hasn't finished yet"""
        self.finished.set()

    def run(self):
        self.finished.wait(self.interval)
        if not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
        self.finished.set()
class LoopTimer(_Timer):
    """Call a function after a specified number of seconds:


            t = LoopTimer(30.0, f, args=[], kwargs={})
            t.start()
            t.cancel()     # stop the timer's action if it's still waiting


    """
    def __init__(self, interval, function, args=[], kwargs={}):
        _Timer.__init__(self,interval, function, args, kwargs)


    def run(self):
        '''''self.finished.wait(self.interval)
        if not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
        self.finished.set()'''
        while True:
            self.finished.wait(self.interval)
            if self.finished.is_set():
                self.finished.set()
                break
            self.function(*self.args, **self.kwargs)
