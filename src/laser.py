import math
import utils


class Laser:
    """
    This class uses the information from the robots lasers to determine
    path related information
    """

    def __init__(self, communicator):
        self.communicator = communicator

    def check_if_circle_safe(self, endx, endy):
        """
        This takes all the lasers and calculates if the circular path to
        endx and endy is unobstructed. endx and endy must be in the robots
        coordinate system i.e. robots position is 0, 0 with heading 0.
        It takes the robot width into account.
        """
        laser_angles = self.communicator.get_laser_angles()
        laser_distances = self.communicator.get_laser_distances()

        robot_width = .45
        radius0 = abs((endx**2+endy**2)/(2*endy))
        radius1 = radius0 + robot_width/2
        radius_1 = radius0 - robot_width/2


        for i in range(min(len(laser_angles),len(laser_distances))):
            if laser_angles[i] > math.pi/2 or laser_angles[i] < -math.pi/2:
                continue # can only hande points in front of robot

            angle = math.pi/2 - utils.sign(endy)*laser_angles[i]

            u0 = math.atan2(endy-utils.sign(endy)*radius0, endx)
            u1 = math.pi/2 + utils.sign(endy)*u0
            u2 = math.pi - u1 - angle

            lt = math.sqrt(radius0**2 + radius_1**2 -
                           radius0*radius_1*math.cos(u1))
            t = u1*radius_1/lt

            if angle > t:
                try:
                    length = radius0*math.cos(angle) + \
                                math.sqrt((radius0*math.cos(angle))**2 +
                                           radius1**2 - radius0**2)
                except ValueError:
                    return False
            else:
                try:
                    length = radius0*math.cos(angle) + \
                                math.sqrt((radius0*math.cos(angle))**2 +
                                           radius_1**2 - radius0**2)
                except ValueError:
                    return False

            if math.pi - angle > u1:
                length_end = radius0 * u1 / u2
                if laser_distances[i] < min(length, length_end):
                    return False
            else:
                if laser_distances[i] < length:
                    return False

        return True


    def is_observable(self, point_x, point_y):
        """Use lasers from robot to determine if point is visible to robot"""

        robot_x, robot_y = 0, 0
        angle = utils.angle_between_two_points(robot_x,robot_y,point_x,point_y)
        length = utils.distance_between_two_points(robot_x,robot_y,
                                                   point_x,point_y)
        laser_distances = self.communicator.get_laser_distances()
        increment = self.communicator.get_laser_angle_increment()

        laser_index = ((3*math.pi)/4+angle)/increment
        upper_index = math.ceil(laser_index)
        lower_index = math.floor(laser_index)
        nearest_laser_distances = laser_distances[lower_index:upper_index]

        for i in range(len(nearest_laser_distances)):
            if nearest_laser_distances[i] < length:
                return False

        return True
