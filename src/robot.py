from time import time

from communicator import Communicator
from path_tracker import PathTracker
from path_tracker import NoPointObservableError
from path import Path
from path import EndOfPathError
import utils

class StartpointIsNotInRangeError(Exception):pass

class Robot:
    """
    This class controls the robots driving by setting speed and angular speed.
    The class also controls the total time and time for one timestep.
    """

    def __init__(self, path_file_name, host="localhost", port="50000"):
        self._communicator = Communicator(host, port)
        self._time_for_new_carrot = 0
        self._path = Path(path_file_name)
        self._path_tracker = PathTracker(self._path,self._communicator)

        self._TARGET_SPEED = 1
        self._speed = self._TARGET_SPEED

        print('Starting robot on host {}:{}'.format(host, port))

    def start(self):
        """Starts timing and make sure the robot moves to it´s first point"""
        self.check_if_start_position()
        self._communicator.post_speed(0, self._speed)

        self.time_taking0 = time()

        t0 = time()
        while True:
            try:
                self.update(t0)
                self._communicator.reset()
            except EndOfPathError:
                time_taking = time() - self.time_taking0
                self._communicator.post_speed(0, 0)
                print('Finished Path with time: {}s'.format(time_taking))
                break
            except NoPointObservableError:
                print('Could not observe any point')
                break

            t0 = time()


    def update(self, prev_time):
        """
        Udates the point where the robot is headed and determine how much
        to turn, in order to get to the selected point.
        """
        self._speed = self._TARGET_SPEED
        x, y = self._communicator.get_position()
        self._time_for_new_carrot += time() - prev_time

        if self._time_for_new_carrot > 0:
            try:
                heading = self._communicator.get_heading()
                gamma = self._path_tracker.get_turn_radius_inverse(x, y, heading)
                turn_speed = gamma*self._speed
            except NoPointObservableError:
                #Make the robot rotate til it sees points to go to
                current_angular_speed=self._communicator.get_angular_speed()
                if current_angular_speed>0:
                    turn_speed=2
                    self._speed=0
                else:
                    turn_speed=-2
                    self._speed=0

            if abs(turn_speed) > 2:
                #print('Turning to fast', turn_speed)
                turn_speed = utils.sign(turn_speed)*2
                self._speed = turn_speed/gamma

            self._communicator.post_speed(turn_speed, self._speed)
            self._time_for_new_carrot = 0


    def check_if_start_position(self):
        """
        Controls if the startposition of the path is within 1 meter of the robot
        """
        x,y=self._communicator.get_position()
        new_x,new_y=self._path.next()

        if utils.distance_between_two_points(new_x,new_y,x,y)<1:
            while True:
                angle = utils.angle_between_two_points(x,y,new_x,new_y)
                new_x,new_y = self._path.next()
                if utils.distance_between_two_points(x,y,new_x,new_y)>1:
                    break
        else:
            raise StartpointIsNotInRangeError()
