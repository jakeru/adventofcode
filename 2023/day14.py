#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-14

import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple
import utils
from utils import Point


def parse_input(input):
    return input.strip().split("\n")


def print_grid(grid):
    pass

def move_rock_north(rocks, pos):
    r = rocks.pop(pos)
    while pos.y > 0 and rocks.get(Point(pos.x, pos.y - 1)) is None:
        pos = Point(pos.x, pos.y - 1)
    rocks[pos] = r


def solve1(entries):
    rocks = {}
    for y, line in enumerate(entries):
        for x, c in enumerate(line):
            if c != '.':
                rocks[Point(x, y)] = c
    print_grid(rocks)

    w = max([p.x for p in rocks]) + 1
    h = max([p.y for p in rocks]) + 1

    for x in range(w):
        for y in range(h):
            r = rocks.get(Point(x, y))
            if r == 'O':
                move_rock_north(rocks, Point(x, y))

    print_grid(rocks)

    total = 0
    for pos, r in rocks.items():
        if r == 'O':
            total += h - pos.y

    return total


def solve2(entries):
    pass


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 136)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), None)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
