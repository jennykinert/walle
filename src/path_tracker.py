"""High level control"""

import utils
from path import EndOfPathError

L = 1 #m

class PathTracker:

    def __init__(self, path):
        self._path = path

    def get_turn_speed(self, current_velocity, robot_x, robot_y, robot_angle):
        last_pos = None
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
                self._path.previous()

        try:
            self._path.previous()
        except EndOfPathError:
            pass
        x, y = utils.translate_coordinates_between_systems(path_x, path_y, robot_x, robot_y, robot_angle)
        print('Global: {}, {}\nLocal: {}, {}\n'.format(path_x, path_y, x, y))
        return 2*y/(L**2) * current_velocity