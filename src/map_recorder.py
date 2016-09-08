
from communicator import Communicator
from utils import distance_between_two_points
from datetime import datetime
import json
import sys

def record(host, port):
    positions = []
    try:
        print('Start recording')
        while True:
            com = Communicator(host, port)
            position_data = com.get_position()
            x = position_data['Pose']['Position']['X']
            y = position_data['Pose']['Position']['Y']
            if len(positions) == 0:
                positions.append((x, y))
            else:
                last_x, last_y = positions[len(positions)-1]
                if distance_between_two_points(x, y, last_x, last_y) > 0.01: # == 1cm
                    positions.append((x, y))

    except KeyboardInterrupt:
        print('Start recording')
        data = []
        for pos in positions:
            data.append({'Pose':{'Position':{'X':pos[0], 'Y':pos[1]}}})

        filename = 'Path-'+datetime.now().strftime('%y.%m.%d-%M.%S')+'.json'
        with open(filename, 'w+') as f:
            json.dump(data, f)
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


