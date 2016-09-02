
from communicator import Communicator
from timers import Interval
from timers import Timed

class Robot:

    def __init__(self, path, host="localhost", port="50000"):
        self.communicator = Communicator(host, port)
        self.start()

    def start(self):
        while(True):
            self.update()

    def update(self):
        pass