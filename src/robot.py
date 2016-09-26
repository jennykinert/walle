from time import time

from communicator import Communicator
from path_tracker import PathTracker
from path_tracker import NoPointObservableError
from path import Path
from path import EndOfPathError
import utils

class StartPointNotInRangeError(Exception):pass

class Robot:
    """
    The robot controls all the behavior and communication with the robot on
    the MRDS system
    """

    def __init__(self, path_file_name, host="localhost", port="50000"):
        self._communicator = Communicator(host, port)
        self._time_for_new_carrot = 0
        self._path = Path(path_file_name)
        self._path_tracker = PathTracker(self._path, self._communicator)

        self._TARGET_SPEED = 1
        self._MAX_TURNING_SPEED = 2

        self._turning_to_find_point = None
        self._TURNING_TO_FIND_POINT_TIME = 7

        print('Starting robot on host {}:{}'.format(host, port))

    def start(self):
        """
        Start the robot and its movement. Is blocking until robots finish
        or determine it cannot finish path
        """

        try:
            self.extend_start_position()
        except StartPointNotInRangeError:
            print('Staring point is not range (1m)')
        else:  
            self._communicator.post_speed(0, self._TARGET_SPEED)
            
            self.time_taking0 = time()

            while True:
                try:
                    self.update()
                    self._communicator.reset()
                except EndOfPathError:
                    time_taking = time() - self.time_taking0
                    self._communicator.post_speed(0, 0)
                    print('Finished Path with time: {}s'.format(time_taking))
                    break
                except NoPointObservableError:
                    print('Could not observe any point')
                    break



    def update(self):
        """
        An update on the robot. Performed once per timestep. Will use robots
        information to set a linear speed and a turning speed
        """
        speed = self._TARGET_SPEED
        x, y = self._communicator.get_position()

        heading = self._communicator.get_heading()
        try:
            gamma = self._path_tracker.get_turn_radius_inverse(x, y, heading)
            turn_speed = gamma*speed

        except NoPointObservableError:
            # Make the robot rotate til it sees points to go to
            current_angular_speed = self._communicator.get_angular_speed()
            turn_speed = utils.sign(current_angular_speed) * \
                                                        self._MAX_TURNING_SPEED
            speed = 0
            if not self._turning_to_find_point:
                self._turning_to_find_point = time()
            else:
                if self._turning_to_find_point - time() > \
                                    self._TURNING_TO_FIND_POINT_TIME:
                    raise NoPointObservableError()

        if abs(turn_speed) > self._MAX_TURNING_SPEED:
            # Limit linear speed as max turning speed is constant
            turn_speed = utils.sign(turn_speed)*self._MAX_TURNING_SPEED
            speed = turn_speed/gamma

        self._communicator.post_speed(turn_speed, speed)


    def extend_start_position(self):
        """
        Skip points on the path to make the starting point a small distance
        forward. This is because the robot might make unecessary turning if the
        starting point happen to be a small distance behind robot
        """
        EXTEND_DISTANCE = 1
        x, y = self._communicator.get_position()
        new_x, new_y = self._path.next()

        if utils.distance_between_two_points(new_x, new_y, x, y) < \
                                                        EXTEND_DISTANCE:
            while True:
                new_x, new_y = self._path.next()
                if utils.distance_between_two_points(x, y, new_x, new_y) > \
                                                                EXTEND_DISTANCE:
                    break
        else:
            raise StartPointNotInRangeError()
