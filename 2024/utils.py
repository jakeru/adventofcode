#!/usr/bin/env python3

# Random utility functions by Jakob Ruhe

import unittest
from collections import namedtuple
import re

ORTHO_DIRS = ("N", "W", "S", "E")
ALL_DIRS = ("N", "NW", "W", "SW", "S", "SE", "E", "NE")

# Set to 1 for positive north and -1 for positive south.
NORTH_INC = -1

DIRS_XY = {
    "N": (0, NORTH_INC),
    "NW": (-1, NORTH_INC),
    "W": (-1, 0),
    "SW": (-1, -NORTH_INC),
    "S": (0, -NORTH_INC),
    "SE": (1, -NORTH_INC),
    "E": (1, 0),
    "NE": (1, NORTH_INC),
}

Point = namedtuple("Point", ["x", "y"])


def ortho_adjacent(center):
    return (Point(center.x + dir_x(d), center.y + dir_y(d)) for d in ORTHO_DIRS)


def all_adjacent(center):
    return (Point(center.x + dir_x(d), center.y + dir_y(d)) for d in ALL_DIRS)


def dir_x(d):
    return DIRS_XY[d][0]


def dir_y(d):
    return DIRS_XY[d][1]


def walk(pos, dir, steps=1):
    return Point(pos.x + dir_x(dir) * steps, pos.y + dir_y(dir) * steps)


def turn(d, steps):
    return ALL_DIRS[(ALL_DIRS.index(d) + steps) % len(ALL_DIRS)]


def opposite_dir(d):
    return turn(d, len(ORTHO_DIRS))


def turn_left(d):
    return turn(d, 2)


def turn_right(d):
    return turn(d, -2)


def split_into_groups(items, group_size):
    num = len(items)
    if num % group_size != 0:
        raise ValueError(f"# items ({num}) is not a multiple of {group_size}")
    return [items[i : i + group_size] for i in range(0, num, group_size)]


def parse_ints(string):
    groups = re.findall(r"-?\d+", string)
    return tuple(map(int, groups))


def parse_unsigned_ints(string):
    groups = re.findall(r"\d+", string)
    return tuple(map(int, groups))


def parse_digits(string):
    return tuple(map(int, filter(str.isdigit, string)))


# Execute tests with:
# python3 -m unittest utils
class TestThis(unittest.TestCase):
    def test_turn_left(self):
        self.assertEqual(turn_left("N"), "W")
        self.assertEqual(turn_left("W"), "S")
        self.assertEqual(turn_left("S"), "E")
        self.assertEqual(turn_left("E"), "N")

    def test_turn_right(self):
        self.assertEqual(turn_right("N"), "E")
        self.assertEqual(turn_right("W"), "N")
        self.assertEqual(turn_right("S"), "W")
        self.assertEqual(turn_right("E"), "S")

    def test_turn(self):
        self.assertEqual(turn("N", 1), "NW")
        self.assertEqual(turn("NW", 1), "W")
        self.assertEqual(turn("W", 1), "SW")
        self.assertEqual(turn("SW", 1), "S")
        self.assertEqual(turn("S", 1), "SE")
        self.assertEqual(turn("SE", 1), "E")
        self.assertEqual(turn("E", 1), "NE")
        self.assertEqual(turn("NE", 1), "N")

    def test_dir_x(self):
        self.assertEqual(dir_x("N"), 0)
        self.assertEqual(dir_x("NW"), -1)
        self.assertEqual(dir_x("W"), -1)
        self.assertEqual(dir_x("SW"), -1)
        self.assertEqual(dir_x("S"), 0)
        self.assertEqual(dir_x("SE"), 1)
        self.assertEqual(dir_x("E"), 1)
        self.assertEqual(dir_x("NE"), 1)

    def test_dir_y(self):
        self.assertEqual(dir_y("N"), NORTH_INC)
        self.assertEqual(dir_y("NW"), NORTH_INC)
        self.assertEqual(dir_y("W"), 0)
        self.assertEqual(dir_y("SW"), -NORTH_INC)
        self.assertEqual(dir_y("S"), -NORTH_INC)
        self.assertEqual(dir_y("SE"), -NORTH_INC)
        self.assertEqual(dir_y("E"), 0)
        self.assertEqual(dir_y("NE"), NORTH_INC)

    def test_opposite_dir(self):
        self.assertEqual(opposite_dir("N"), "S")
        self.assertEqual(opposite_dir("S"), "N")
        self.assertEqual(opposite_dir("W"), "E")
        self.assertEqual(opposite_dir("E"), "W")

    def test_split_into_groups(self):
        self.assertEqual(split_into_groups((1, 2, 3, 4), 2), [(1, 2), (3, 4)])
        with self.assertRaises(ValueError):
            split_into_groups((1, 2, 3, 4), 3)

    def test_parse_ints(self):
        self.assertEqual(parse_ints(""), ())
        self.assertEqual(parse_ints("no digits"), ())
        self.assertEqual(parse_ints("123"), (123,))
        self.assertEqual(parse_ints("123,-456,789"), (123, -456, 789))
        self.assertEqual(parse_ints("hello12,3world 4567."), (12, 3, 4567))

    def test_parse_unsigned_ints(self):
        self.assertEqual(parse_unsigned_ints(""), ())
        self.assertEqual(parse_unsigned_ints("no digits"), ())
        self.assertEqual(parse_unsigned_ints("123,-456,789"), (123, 456, 789))
        self.assertEqual(parse_unsigned_ints("2-6,4-8"), (2, 6, 4, 8))

    def test_parse_digits(self):
        self.assertEqual(parse_digits(""), ())
        self.assertEqual(parse_digits("abc"), ())
        self.assertEqual(parse_digits("1"), (1,))
        self.assertEqual(parse_digits("ab123c4"), (1, 2, 3, 4))
