from time import time

from communicator import Communicator
from path_tracker import PathTracker
from path_tracker import NoPointObservableError
from path import Path
from path import EndOfPathError
import math
import utils

class StartpointIsNotInRangeError(Exception):pass

class Robot:

    def __init__(self, path_file_name, host="localhost", port="50000"):
        self._communicator = Communicator(host, port)
        self._time_for_new_carrot = 0
        self._path = Path(path_file_name)
        self._path_tracker = PathTracker(self._path,self._communicator)

        self._TARGET_SPEED = 1
        self._speed = self._TARGET_SPEED

        print('Starting robot on host {}:{}'.format(host, port))

    def start(self):
        self.check_if_start_position()
        self._communicator.post_speed(0, self._speed)
        t0 = time()
        while True:
            try:
                self.update(t0)
                self._communicator.reset()
            except EndOfPathError:
                self._communicator.post_speed(0, 0)
                print('Finished Path')
                break
            except NoPointObservableError:
                print('Could not observe any point')
                break

            t0 = time()


    def update(self, prev_time):
        self._speed = self._TARGET_SPEED
        x, y = self._communicator.get_position()
        self._time_for_new_carrot += time() - prev_time

        if self._time_for_new_carrot > .01:
            try:
                heading = self._communicator.get_heading()
                gamma = self._path_tracker.get_turn_radius_inverse(x, y, heading)
                turn_speed = gamma*self._speed
            except NoPointObservableError:
                #Make the robot rotate til it sees points to go to
                current_angular_speed=self._communicator.get_angular_speed()
                if current_angular_speed>0:
                    turn_speed=2
                    speed=0
                else:
                    turn_speed=-2
                    speed=0

            #print('turn speed', turn_speed)
            if abs(turn_speed) > 2:
                print('Turning to fast', turn_speed)
                turn_speed = math.copysign(1, turn_speed)*2
                self._speed = turn_speed/gamma

            self._communicator.post_speed(turn_speed, self._speed)
            self._time_for_new_carrot = 0


    def check_if_start_position(self):
        x,y=self._communicator.get_position()
        new_x,new_y=self._path.next()

        if utils.distance_between_two_points(new_x,new_y,x,y)<0.2:
            while True:
                angle=utils.angle_between_two_points(x,y,new_x,new_y)
                new_x,new_y = self._path.next()
                if utils.distance_between_two_points(x,y,new_x,new_y)>0.2:
                    break
        else:
            raise StartpointIsNotInRangeError()
