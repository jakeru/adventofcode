#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-13

import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple
import utils
from utils import Point


def parse_input(input):
    return input.strip().split("\n")


def is_mirror_at_x(grid, x, w, h):
    num_wrong = 0
    for i in range(w):
        for y in range(h):
            p1 = Point(x - i - 1, y)
            p2 = Point(x + i, y)
            g1 = grid.get(p1)
            g2 = grid.get(p2)
            if g1 is not None and g2 is not None and g1 != g2:
                num_wrong += 1
    if num_wrong == 0:
        print(f"Found mirror at x: {x}")
    elif num_wrong == 1:
        print(f"Found smudge mirror at x: {x}")
    return num_wrong


def is_mirror_at_y(grid, y, w, h):
    num_wrong = 0
    for i in range(h):
        for x in range(w):
            p1 = Point(x, y - i - 1)
            p2 = Point(x, y + i)
            g1 = grid.get(p1)
            g2 = grid.get(p2)
            if g1 is not None and g2 is not None and g1 != g2:
                num_wrong += 1
    if num_wrong == 0:
        print(f"Found mirror at y: {y}")
    elif num_wrong == 1:
        print(f"Found smudge mirror at y: {y}")
    else:
        print(f"Found no mirror at y: {y} num_wrong: {num_wrong}")
    return num_wrong


def find_mirrors_in_grid(grid, num_smudged):
    w = max([p.x for p in grid.keys()]) + 1
    h = max([p.y for p in grid.keys()]) + 1
    total = 0

    for x in range(1, w):
        if is_mirror_at_x(grid, x, w, h) == num_smudged:
            total += x

    for y in range(1, h):
        if is_mirror_at_y(grid, y, w, h) == num_smudged:
            total += 100 * y

    return total


def print_grid(grid):
    w = max([p.x for p in grid.keys()]) + 1
    h = max([p.y for p in grid.keys()]) + 1
    for y in range(h):
        line = []
        for x in range(w):
            line.append(grid.get(Point(x, y)))
        print("".join(line))


def solve1(entries):
    patterns = []
    grid = {}
    y = 0
    for line in entries:
        if not line:
            y = 0
            patterns.append(grid)
            grid = {}
            continue
        for x, c in enumerate(line):
            grid[Point(x, y)] = c
        y += 1
    if grid:
        patterns.append(grid)

    total = 0
    for grid in patterns:
        print("A grid:")
        print_grid(grid)
        total += find_mirrors_in_grid(grid, 0)
        print("")

    return total


def solve2(entries):
    patterns = []
    grid = {}
    y = 0
    for line in entries:
        if not line:
            y = 0
            patterns.append(grid)
            grid = {}
            continue
        for x, c in enumerate(line):
            grid[Point(x, y)] = c
        y += 1
    if grid:
        patterns.append(grid)

    total = 0
    for grid in patterns:
        print("A grid:")
        print_grid(grid)
        total += find_mirrors_in_grid(grid, 1)
        print("")

    return total


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 405)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 400)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
