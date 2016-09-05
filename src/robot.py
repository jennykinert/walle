from time import time
from math import pi

from communicator import Communicator
import steering
from timers import Interval
from timers import Timed
from utils import distance_between_two_points
from utils import angle_between_two_points
from utils import angle_within

class Robot:

    def __init__(self, path, host="localhost", port="50000"):
        self.communicator = Communicator(host, port)
        self.start()

    def start(self):
        x, y = self.communicator.get_position()
        #distans = distance_between_two_points(x, y, 1, 0)
        self.steering = steering.Steering(pi/2)
        t0 = time()
        while True:
            self.update(t0)
            t0 = time()


    def update(self, prev_time):
        #x, y = self.communicator.get_position()
        #distans_left = distance_between_two_points(x, y, 1, 0)
        #angle = angle_between_two_points(x, y, 1, 0)
        heading = self.communicator.get_heading()
        #if not angle_within(heading, angle):
        #    distans_left *= -1

        #print(distans_left)
        self.communicator.post_speed(self.steering.new_speed(pi/2 - heading, time() - prev_time), 0)