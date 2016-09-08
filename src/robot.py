from time import time
from math import pi

from communicator import Communicator
from path_tracker import PathTracker
from path import Path
from path import EndOfPathError
from laser import Laser
import steering
from timers import Interval
from timers import Timed
import utils

class Robot:

    def __init__(self, path_file_name, host="localhost", port="50000"):
        self.communicator = Communicator(host, port)
        self._time_for_new_carrot = 0
        self._path = Path(path_file_name)
        self._path_tracker = PathTracker(self._path)
        self._laser = Laser(self.communicator)

        self._speed = 1
        self._allowed_to_check_end = False

        print('Starting robot on host {}:{}'.format(host, port))

    def start(self):

        x, y = self.communicator.get_position()
        #distans = distance_between_two_points(x, y, 1, 0)
        self.steering = steering.Steering(pi/2)
        t0 = time()
        self.communicator.post_speed(0, self._speed)
        start_time = time()
        while True:
            if time() - start_time > 10:
                self._allowed_to_check_end = True

            try:
                self.update(t0)
            except EndOfPathError:
                self.communicator.post_speed(0, 0)
                print('Finished Path')
                break

            t0 = time()


    def update(self, prev_time):
        x, y = self.communicator.get_position()
        #distans_left = distance_between_two_points(x, y, 1, 0)
        #angle = angle_between_two_points(x, y, 1, 0)

        self._time_for_new_carrot += time() - prev_time
        if self._time_for_new_carrot > .1:
            heading = self.communicator.get_heading()
            if self._allowed_to_check_end:
                robot_x, robot_y = self.communicator.get_position()
                end_x, end_y = self._path.get_last_position()
                translated_x, translated_y = utils.translate_coordinates_between_systems(end_x, end_y, robot_x, robot_y, heading)
                if self._laser.is_observable(translated_x, translated_y):
                    if self._laser.check_if_circle_safe(translated_x,translated_y):
                        turn_speed = self._path_tracker.get_turn_speed_to_point(self._speed, x, y, heading, end_x, end_y)
                    else:
                        turn_speed = self._path_tracker.get_turn_speed(self._speed, x, y, heading)
                else:
                    turn_speed = self._path_tracker.get_turn_speed(self._speed, x, y, heading)
            else:
                turn_speed = self._path_tracker.get_turn_speed(self._speed, x, y, heading)
            self.communicator.post_speed(turn_speed, self._speed)
            self._time_for_new_carrot = 0

        #if not angle_within(heading, angle):
        #    distans_left *= -1

        #print(distans_left)
        #self.communicator.post_speed(self.steering.new_speed(pi/2 - heading, time() - prev_time), 0)
