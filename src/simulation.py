
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
            Robot(path, host=host, port=port).start()

        elif len(sys.argv) > 2:
            path = sys.argv[1]
            host = sys.argv[2]
            Robot(path, host=host).start()

        elif len(sys.argv) > 1:
            path = sys.argv[1]
            Robot(path).start()

        else:

            Robot('Paths/Path-around-table-and-back.json').start()
            #print("Must provide file path to json path")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exit')
    except ConnectionRefusedError:
        print('Could not connect to server')
    except (ConnectionResetError, TimeoutError):
        print('Lost connection to simulation')
