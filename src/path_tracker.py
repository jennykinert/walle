"""High level control"""

import utils
from path import EndOfPathError
from laser import Laser

L = 1 #m

class NoPointObservableError(Exception):pass
class PathTracker:

    def __init__(self, path,communicator):
        self._path = path
        self._laser = Laser(communicator)

    def get_turn_radius_inverse(self, robot_x, robot_y, robot_angle):
        """last_pos = None
        while True:
            path_x, path_y = self._path.next()
            if L < utils.distance_between_two_points(path_x, path_y, robot_x, robot_y):
                break
            last_pos = (path_x, path_y)

        if last_pos:
            last_distance = utils.distance_between_two_points(last_pos[0], last_pos[1], robot_x, robot_y)
            current_distance = utils.distance_between_two_points(path_x, path_y, robot_x, robot_y)
            if L - last_distance < current_distance - L:
                path_x = last_pos[0]
                path_y = last_pos[1]
                self._path.previous()"""

        path_x,path_y=self.get_next_point(robot_x,robot_y,robot_angle)
        print(path_x,path_y)
        try:
            self._path.previous()
        except EndOfPathError:
            pass
        return self.get_turn_radius_inverse_to_point(path_x, path_y)

    def get_turn_radius_inverse_to_point(self,x,y):

        L_adjusted = utils.distance_between_two_points(0, 0, x, y)

        return 2*y/(L_adjusted**2)

    def get_next_point(self, robot_x,robot_y,robot_angle):
        backtracking=False
        while True:

            x,y=self._path.next()
            translated_x, translated_y = utils.translate_coordinates_between_systems(x, y, robot_x, robot_y, robot_angle)

            if not self._laser.is_observable(translated_x,translated_y):
                try:
                    path_x
                except NameError:
                    backtracking=True
                break
            path_x,path_y=translated_x,translated_y

        if backtracking:
            while True:
                x,y=self._path.previous()
                translated_x, translated_y = utils.translate_coordinates_between_systems(x, y, robot_x, robot_y, robot_angle)
                if self._laser.is_observable(translated_x, translated_y):
                    path_x,path_y=translated_x,translated_y
                    break

        try:
            while True:
                if self._laser.check_if_circle_safe(path_x,path_y):
                    return path_x,path_y
                else:
                    x,y=self._path.previous()
                    path_x, path_y = utils.translate_coordinates_between_systems(x, y, robot_x, robot_y, robot_angle)

        except NameError:
            raise NoPointObservableError()
