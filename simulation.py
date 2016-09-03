
import sys
from robot import Robot


def main():
    if len(sys.argv) > 1 and \
            (sys.argv[1] == '-h' or sys.argv[1] == '-help' or sys.argv[1] == '--help'):
        print('usage: {} path_to_track [host] [port]\n'.format(sys.argv[0]))

    else:
        if len(sys.argv) > 3:
            path = sys.argv[1]
            host = sys.argv[2]
            port = sys.argv[3]
            print('Starting robot on host {}:{}'.format(host, port))
            Robot(path, host=host, port=port)

        elif len(sys.argv) > 2:
            path = sys.argv[1]
            host = sys.argv[2]
            print('Starting robot on host {}'.format(host))
            Robot(path, host=host)

        elif len(sys.argv) > 1:
            path = sys.argv[1]
            print('Starting robot')
            Robot(path)

        else:
            Robot('Paths/Path-to-bed.json')
            #print("Must provide file path to json path")
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exit')
    except ConnectionResetError:
        print('Lost connection to simulation')