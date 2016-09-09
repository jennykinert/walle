from time import time

from communicator import Communicator
from path_tracker import PathTracker
from path_tracker import NoPointObservableError
from path import Path
from path import EndOfPathError

class Robot:

    def __init__(self, path_file_name, host="localhost", port="50000"):
        self._communicator = Communicator(host, port)
        self._time_for_new_carrot = 0
        self._path = Path(path_file_name)
        self._path_tracker = PathTracker(self._path,self._communicator)

        self._speed = .5

        print('Starting robot on host {}:{}'.format(host, port))

    def start(self):
        t0 = time()
        self._communicator.post_speed(0, self._speed)
        while True:
            try:
                self.update(t0)
                self._communicator.reset()
            except EndOfPathError:
                heading = self._communicator.get_heading()
                x, y = self._communicator.get_last_position()
                gamma = self._path_tracker.get_turn_radius_inverse(x, y, heading)
                turn_speed = gamma*self._speed
                self._communicator.post_speed(turn_speed, self._speed)
                print('Finished Path')
                break
            except NoPointObservableError:
                print('Could not observe any point')
                break

            t0 = time()


    def update(self, prev_time):
        self._speed = .5
        x, y = self._communicator.get_position()
        self._time_for_new_carrot += time() - prev_time

        if self._time_for_new_carrot > .1:
            heading = self._communicator.get_heading()
            gamma = self._path_tracker.get_turn_radius_inverse(x, y, heading)
            turn_speed = gamma*self._speed
            print('turn speed', turn_speed)
            if turn_speed > 2: # TODO Check -2 also
                turn_speed = 2
                self._speed = turn_speed/gamma
                
            self._communicator.post_speed(turn_speed, self._speed)
            self._time_for_new_carrot = 0
