import unittest
import math
from math import radians

from src import utils

class UtilsTest(unittest.TestCase):

    def test_angle_within_half_circle(self):
        self.assertTrue(utils.angle_within(radians(10), radians(-10)))
        self.assertTrue(utils.angle_within(radians(-170), radians(170)))

    def test_angle_not_within_half_circle(self):
        self.assertFalse(utils.angle_within(radians(171), radians(-10)))
        self.assertFalse(utils.angle_within(radians(160), radians(-100)))

    def test_angle_within_ten_degrees(self):
        self.assertTrue(utils.angle_within(radians(-1), radians(-10), range=radians(10)))

    def test_angle_not_within_ten_degrees(self):
        self.assertFalse(utils.angle_within(radians(1), radians(-10), range=radians(10)))


    def test_normalize_angle(self):
        self.assertTrue(math.isclose(utils.normalize_angle(radians(360+1)), radians(1)))
        self.assertTrue(math.isclose(utils.normalize_angle(radians(-360-50)), radians(-50)))
        self.assertTrue(math.isclose(utils.normalize_angle(radians(-360-190)), radians(170)))
        self.assertTrue(math.isclose(utils.normalize_angle(radians(-360*5-190)), radians(170)))

    def test_angle_defference(self):
        self.assertTrue(math.isclose(utils.angle_difference(radians(-170), radians(170)), radians(-20)))
        self.assertTrue(math.isclose(utils.angle_difference(radians(0), radians(-80)), radians(-80)))

    def test_worldcoordinate_to_robotcoordinate(self):
        x,y=utils.worldcoordinate_to_robotcoordinate(2,2,1,1,math.pi/4)
        print(x,y)
        self.assertTrue(math.isclose(x,math.sqrt(2)))
        self.assertTrue(math.isclose(y,0))

    def test_worldcoordinate_to_robotcoordinate2(self):
        x,y=utils.worldcoordinate_to_robotcoordinate(0,2,2,2,radians(-135))
        self.assertTrue(math.isclose(x,-math.cos(math.pi/4)*2))
        self.assertTrue(math.isclose(y, math.sin(math.pi/4)*2))
