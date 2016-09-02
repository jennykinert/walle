
from communicator import Communicator
from timers import Interval
from timers import Timed

class Robot:

    def __init__(self, path, host="localhost", port="50000"):
        self.communicator = Communicator(host, port)
        self.start()

    def start(self):
        Interval(1, self.update)

    def update(self):
        print(1)#self.communicator.get