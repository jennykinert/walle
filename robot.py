
from communicator import Communicator
import steering
from timers import Interval
from timers import Timed
from utils import distance_between_two_points
from utils import angle_between_two_points
from utils import angle_within_half_circle

class Robot:

    def __init__(self, path, host="localhost", port="50000"):
        self.communicator = Communicator(host, port)
        self.start()

    def start(self):
        x, y = self.communicator.get_position()
        distans = distance_between_two_points(x, y, 1, 0)
        self.steering = steering.Distance(distans)
        while(True):
            self.update()

    def update(self):
        x, y = self.communicator.get_position()
        distans_left = distance_between_two_points(x, y, 1, 0)
        angle = angle_between_two_points(x, y, 1, 0)
        heading = self.communicator.get_heading()
        if angle_within(heading, angle):
            distans_left *= -1
            print(-1)
        #print(distans_left)
        self.communicator.post_speed(0, self.steering.new_speed(distans_left))