"""High level control"""

import math
import utils
from path import EndOfPathError
from laser import Laser

class NoPointObservableError(Exception):pass


class PathTracker:
    """
    Uses Pure Pursuit to determine next position in path to take.
    Chooses point based on observability and collision detection.
    """

    def __init__(self, path, communicator):
        self._path = path
        self._laser = Laser(communicator)

    def get_turn_radius_inverse(self, robot_x, robot_y, robot_angle):
        """
        Get radius inverse, also called gamma, for the circle based upon the
        robots coordinates a goal point which is chosen.
        Will raise EndOfPathError if robot is within 1 m of end of path
        """

        try:
            path_x, path_y = self.get_next_point(robot_x,robot_y,robot_angle)

        except EndOfPathError:
            x, y = self._path.get_last_position()
            path_x, path_y = utils.translate_coordinates_between_systems(x, y, robot_x, robot_y, robot_angle)

            if utils.distance_between_two_points(0, 0, path_x, path_y) < 1:
                raise EndOfPathError('Within 1m of end of path')

            if not self._laser.check_if_circle_safe(path_x,path_y):
                while True:
                    x, y = self._path.previous()
                    translated_x, translated_y = utils.translate_coordinates_between_systems(x, y, robot_x, robot_y, robot_angle)
                    if self._laser.check_if_circle_safe(translated_x, translated_y):
                        path_x, path_y = translated_x, translated_y
                        break

        try:
            self._path.previous()
        except EndOfPathError:
            pass
        return self.get_turn_radius_inverse_to_point(path_x, path_y)


    def get_turn_radius_inverse_to_point(self, x, y):
        """Performs Pure Pursuit Algorithms formula to calculate radius inverse"""

        L_adjusted = utils.distance_between_two_points(0, 0, x, y)
        angle = utils.angle_between_two_points(0, 0, x, y)

        if abs(angle) > math.pi/2:
            return 9999999*utils.sign(angle)

        if abs(angle) > math.pi/2:
            angle = utils.sign(angle) * math.pi/2

        if abs(angle) == math.pi/2:
            angle -= utils.sign(angle)*0.0001

        gamma = (2*y)/(L_adjusted**2)

        return gamma


    def get_next_point(self, robot_x, robot_y, robot_angle):
        """
        Get next point to which is viable to travel to. Will base 
        viability on that point must be visible and able to be traveled to without collision
        """

        backtracking = False

        while True:

            x, y = self._path.next()
            translated_x, translated_y = utils.translate_coordinates_between_systems(x, y, robot_x, robot_y, robot_angle)

            if not self._laser.is_observable(translated_x,translated_y):
                try:
                    path_x
                except NameError:
                    backtracking=True
                break

            path_x,path_y = translated_x,translated_y


        if backtracking:
            while True:
                x, y = self._path.previous()
                translated_x, translated_y = utils.translate_coordinates_between_systems(x, y, robot_x, robot_y, robot_angle)
                if self._laser.is_observable(translated_x, translated_y):
                    path_x, path_y = translated_x, translated_y
                    break

        try:
            while True:
                if self._laser.check_if_circle_safe(path_x,path_y):
                    return path_x, path_y
                else:
                    try:
                        x, y = self._path.previous()
                        path_x, path_y = utils.translate_coordinates_between_systems(x, y, robot_x, robot_y, robot_angle)
                    except EndOfPathError:
                        raise NoPointObservableError()

        except NameError:
            raise NoPointObservableError()
