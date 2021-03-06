"""
Script to record a path driven by the robot.

Takes to optional argument
arg1: ip-address (default: localhost)
arg2: port (default: 50000)

Will finish and save to file on ctrl-c. 
File name will be in form of Path-<data>-<time>.json
"""


from communicator import Communicator
from utils import distance_between_two_points
from datetime import datetime
import json
import sys

def record(host, port):
    positions = []
    try:
        print('Start recording')

        com = Communicator(host, port)
        while True:
            position_data = com.get_position_data()
            x = position_data['Pose']['Position']['X']
            y = position_data['Pose']['Position']['Y']
            if len(positions) == 0:
                positions.append(position_data)
            else:
                last_position_data = positions[len(positions)-1]
                last_x = last_position_data['Pose']['Position']['X']
                last_y = last_position_data['Pose']['Position']['Y']
                if distance_between_two_points(x, y, last_x, last_y) > 0.01:#m
                    positions.append(position_data)

    except KeyboardInterrupt:
        print('Stopped recording')

        filename = 'Path-'+datetime.now().strftime('%y.%m.%d-%M.%S')+'.json'
        with open(filename, 'w+') as f:
            json.dump(positions, f)
        print('Saved path to file: '+filename)
        

if __name__ == '__main__':
    try:
        host = sys.argv[1]
    except IndexError:
        host = 'localhost'

    try:
        port = sys.argv[2]
    except IndexError:
        port = '50000'

    record(host, port)


