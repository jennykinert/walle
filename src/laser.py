"""
This class retrieves information from the lasers. It can get information from
all lasers or specific lasers.
"""
import math
import utils
class Laser:
    def __init__(self, communicator):
        self.communicator = communicator

    def check_if_circle_safe(self,endx, endy):
        laser_angles=self.communicator.get_laser_angles()
        laser_distances  = self.communicator.get_laser_distance()
        laser_angles,laser_distances=self.extract_lasers_in_range(laser_angles,
                laser_distances,0,0,endx,endy)
        radius=(endx**2+endy**2)/(2*endy)

        for i in range(min(len(laser_angles),len(laser_distances))):
            angle=laser_angles[i]
            angle_between_length_and_radius= 3*math.pi/4-angle
            length=2*radius*math.cos(angle_between_length_and_radius)
            if laser_distances[i]<length:
                return False

        return True

    def extract_lasers_in_range(self,laser_angles,laser_distances,startx,starty,endx,endy):
        angle_range=utils.angle_between_two_points(startx,starty,endx,endy)
        increment=self.communicator.get_laser_angle_increment()
        number_of_lasers=math.ceil((3*math.pi/4+angle_range)/increment)
        print(number_of_lasers, len(laser_angles)//2)
        if angle_range<0:
            laser_angles_in_range=laser_angles[number_of_lasers:len(laser_angles)//2]
            laser_distances_in_range=laser_distances[number_of_lasers:len(laser_distances)//2]
            return laser_angles_in_range, laser_distances_in_range
        else:
            laser_angles_in_range=laser_angles[len(laser_angles)//2:number_of_lasers]
            laser_distances_in_range=laser_distances[len(laser_distances)//2:number_of_lasers]
            return laser_angles_in_range, laser_distances_in_range



    def is_observable(self, point_x, point_y):
        robot_x, robot_y = 0, 0
        angle=utils.angle_between_two_points(robot_x,robot_y,point_x,point_y)
        length= utils.distance_between_two_points(robot_x,robot_y,point_x,point_y)
        laser_distances  = self.communicator.get_laser_distance()
        increment=self.communicator.get_laser_angle_increment()

        laser_index=((3*math.pi)/4+angle)/increment
        upper_index=math.ceil(laser_index)
        lower_index=math.floor(laser_index)
        nearest_laser_distances=laser_distances[lower_index:upper_index]
        for i in range(len(nearest_laser_distances)):
            if nearest_laser_distances[i]<length:
                return False
        return True
