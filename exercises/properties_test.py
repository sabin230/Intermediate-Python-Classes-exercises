"""Tests for property exercises"""
import math
import unittest

from properties import Circle, Vector, Person


class CircleTests(unittest.TestCase):

    """Tests for Circle."""

    def test_radius(self):
        circle = Circle(5)
        self.assertEqual(circle.radius, 5)

    def test_default_radius(self):
        circle = Circle()
        self.assertEqual(circle.radius, 1)

    def test_diameter_changes(self):
        circle = Circle(2)
        self.assertEqual(circle.diameter, 4)
        circle.radius = 3
        self.assertEqual(circle.diameter, 6)

    def test_set_diameter(self):
        circle = Circle(2)
        self.assertEqual(circle.diameter, 4)
        circle.diameter = 3
        self.assertEqual(circle.radius, 1.5)

    def test_area(self):
        circle = Circle(2)
        self.assertEqual(circle.area, math.pi * 4)

    @unittest.skip("Log Radius Changes")
    def test_radius_changes_logged(self):
        circle = Circle(2)
        self.assertEqual(circle.radius_changes, [2])
        circle.radius = 3
        self.assertEqual(circle.radius_changes, [2, 3])
        circle.diameter = 3
        self.assertEqual(circle.radius_changes, [2, 3, 1.5])

    @unittest.skip("Set Radius Error")
    def test_no_negative_radius(self):
        circle = Circle(2)
        with self.assertRaises(ValueError) as context:
            circle.radius = -10
        self.assertEqual(str(context.exception), "Radius cannot be negative!")


class VectorTests(unittest.TestCase):

    """Tests for Vector."""

    def test_attributes(self):
        v = Vector(1, 2, 3)
        self.assertEqual((v.x, v.y, v.z), (1, 2, 3))

    def test_magnitude_property(self):
        v = Vector(2, 3, 6)
        self.assertEqual(v.magnitude, 7.0)
        try:
            v.y = 9
        except AttributeError:
            v = Vector(2, 9, 6)
        self.assertEqual(v.magnitude, 11.0)

    def test_no_weird_extras(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(4, 5, 6)
        with self.assertRaises(TypeError):
            len(v1)
        with self.assertRaises(TypeError):
            v1 < v2
        with self.assertRaises(TypeError):
            v1 > v2
        with self.assertRaises(TypeError):
            v1 <= v2
        with self.assertRaises(TypeError):
            v1 >= v2
        with self.assertRaises(TypeError):
            v1 + (1, 2, 3)
        with self.assertRaises(TypeError):
            (1, 2, 3) + v1
        with self.assertRaises(TypeError):
            v1 - (1, 2, 3)
        with self.assertRaises(TypeError):
            v1 * 'a'
        with self.assertRaises(TypeError):
            v1 / v2

    @unittest.skip("Vector Equality")
    def test_equality_and_inequality(self):
        self.assertNotEqual(Vector(1, 2, 3), Vector(1, 2, 4))
        self.assertEqual(Vector(1, 2, 3), Vector(1, 2, 3))
        self.assertFalse(Vector(1, 2, 3) != Vector(1, 2, 3))
        v1 = Vector(1, 2, 3)
        v2 = Vector(1, 2, 4)
        v3 = Vector(1, 2, 3)
        self.assertNotEqual(v1, v2)
        self.assertEqual(v1, v3)

    @unittest.skip("Vector Adding")
    def test_shifting(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(4, 5, 6)
        v3 = v2 + v1
        v4 = v3 - v1
        self.assertEqual((v3.x, v3.y, v3.z), (5, 7, 9))
        self.assertEqual((v4.x, v4.y, v4.z), (v2.x, v2.y, v2.z))

    @unittest.skip("Vector Multiplying")
    def test_scaling(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(4, 5, 6)
        v3 = v1 * 4
        v4 = 2 * v2
        self.assertEqual((v3.x, v3.y, v3.z), (4, 8, 12))
        self.assertEqual((v4.x, v4.y, v4.z), (8, 10, 12))

    @unittest.skip("Vector Iterability")
    def test_multiple_assignment(self):
        x, y, z = Vector(x=1, y=2, z=3)
        self.assertEqual((x, y, z), (1, 2, 3))

    @unittest.skip("Vector Immutability")
    def test_immutability(self):
        v1 = Vector(1, 2, 3)
        with self.assertRaises(Exception):
            v1.x = 4
        self.assertEqual(v1.x, 1)


class PersonTests(unittest.TestCase):

    """Tests for Person."""

    def test_construct(self):
        Person("Trey", "Hunner")

    def test_first_and_last_name_attributes(self):
        trey = Person("Trey", "Hunner")
        self.assertEqual(trey.first_name, "Trey")
        self.assertEqual(trey.last_name, "Hunner")

    def test_name_attribute(self):
        trey = Person("Trey", "Hunner")
        self.assertEqual(trey.name, "Trey Hunner")

    def test_change_names(self):
        trey = Person("Trey", "Hunner")
        trey.last_name = "Smith"
        self.assertEqual(trey.name, "Trey Smith")
        trey.first_name = "John"
        self.assertEqual(trey.name, "John Smith")


if __name__ == "__main__":
    from helpers import error_message
    error_message()
