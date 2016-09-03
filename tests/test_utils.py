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