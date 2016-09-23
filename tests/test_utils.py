import unittest
import math
from math import radians

from src import utils

class UtilsTest(unittest.TestCase):
    """
    Test cases for the mathematical parts of the utils module.
    """

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

    def test_angle_difference(self):
        self.assertTrue(math.isclose(utils.angle_difference(radians(-170), radians(170)), radians(-20)))
        self.assertTrue(math.isclose(utils.angle_difference(radians(0), radians(-80)), radians(-80)))

    def test_translate_coordinates_between_systems_quadrant_1(self):
        try:
            expected_x, expected_y = math.sqrt(2), 0
            x,y = utils.translate_coordinates_between_systems(2 ,2, 1, 1, math.pi/4)
            self.assertTrue(math.isclose(x, expected_x))
            self.assertTrue(math.isclose(y, expected_y))
        except AssertionError:
            raise AssertionError('x: {} should be {}, y: {} should be {}'.format(x, expected_x, y, expected_y))


    def test_translate_coordinates_between_systems_quadrant_3(self):
        try:
            expected_x, expected_y = -math.cos(math.pi/4)*2, math.sin(math.pi/4)*2
            x,y = utils.translate_coordinates_between_systems(0, 2 , 2, 2, radians(-135))
            self.assertTrue(math.isclose(x, expected_x))
            self.assertTrue(math.isclose(y, expected_y))
        except AssertionError:
            raise AssertionError('x: {} should be {}, y: {} should be {}'.format(x, expected_x, y, expected_y))

    def test_translate_coordinates_between_systems_quadrant_2(self):
        try:
            expected_x, expected_y = 3, 1
            x,y = utils.translate_coordinates_between_systems(1, 4, 2, 1, radians(90))
            self.assertTrue(math.isclose(x, expected_x))
            self.assertTrue(math.isclose(y, expected_y))
        except AssertionError:
            raise AssertionError('x: {} should be {}, y: {} should be {}'.format(x, expected_x, y, expected_y))

    def test_translate_coordinates_between_systems_quadrant_2_2(self):
        try:
            expected_x, expected_y = -2, 3
            x,y = utils.translate_coordinates_between_systems(-1, -4, 2, -2, radians(90))
            self.assertTrue(math.isclose(x, expected_x))
            self.assertTrue(math.isclose(y, expected_y))
        except AssertionError:
            raise AssertionError('x: {} should be {}, y: {} should be {}'.format(x, expected_x, y, expected_y))

    def test_translate_coordinates_between_systems3(self):
        try:
            expected_x, expected_y = 0, 0
            x, y = utils.translate_coordinates_between_systems(0, 0, 0, 0, 0)
            self.assertTrue(math.isclose(x, expected_x))
            self.assertTrue(math.isclose(y, expected_y))
        except AssertionError:
            raise AssertionError('x: {} should be {}, y: {} should be {}'.format(x, expected_x, y, expected_y))

    def test_translate_coordinates_between_systems4(self):
        try:
            expected_x, expected_y = 3, 4
            x, y = utils.translate_coordinates_between_systems(3, 4, 0, 0, 0)
            self.assertTrue(math.isclose(x, expected_x))
            self.assertTrue(math.isclose(y, expected_y))
        except AssertionError:
            raise AssertionError('x: {} should be {}, y: {} should be {}'.format(x, expected_x, y, expected_y))
