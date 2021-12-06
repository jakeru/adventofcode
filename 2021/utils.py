#!/usr/bin/env python3

import unittest

DIRS = ("N", "W", "S", "E")

def dir_from_name(name):
    return DIRS.index(name)

def dir_name(d):
    return DIRS[d]

def dir_x(d):
    return (0, -1, 0, 1)[d]

def dir_y(d):
    return (1, 0, -1, 0)[d]

def turn_left(d):
    return (d + 1) % len(DIRS)

def turn_right(d):
    return (d - 1) % len(DIRS)

# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    def test1(self):
        self.assertEqual(turn_left(dir_from_name("N")), dir_from_name("W"))
        self.assertEqual(turn_left(dir_from_name("W")), dir_from_name("S"))
        self.assertEqual(turn_left(dir_from_name("S")), dir_from_name("E"))
        self.assertEqual(turn_left(dir_from_name("E")), dir_from_name("N"))
        self.assertEqual(turn_right(dir_from_name("N")), dir_from_name("E"))
        self.assertEqual(turn_right(dir_from_name("W")), dir_from_name("N"))
        self.assertEqual(turn_right(dir_from_name("S")), dir_from_name("W"))
        self.assertEqual(turn_right(dir_from_name("E")), dir_from_name("S"))
