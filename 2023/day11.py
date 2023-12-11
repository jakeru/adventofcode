#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-11

import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple
import utils
from utils import Point
import itertools


def parse_input(input):
    return input.strip().split("\n")


def expand_rows(grid):
    w = max([p.x for p in grid.keys()]) + 1
    h = max([p.y for p in grid.keys()]) + 1
    dy = 0
    grid_out = {}
    for y in range(h):
        found = []
        for x in range(w):
            if grid.get(Point(x, y)):
                found.append(Point(x, y))
        if found:
            for p in found:
                grid_out[Point(p.x, dy)] = "#"
            dy += 1
        else:
            dy += 2
    return grid_out


def expand_cols(grid):
    w = max([p.x for p in grid.keys()]) + 1
    h = max([p.y for p in grid.keys()]) + 1
    dx = 0
    grid_out = {}
    for x in range(w):
        found = []
        for y in range(h):
            if grid.get(Point(x, y)):
                found.append(Point(x, y))
        if found:
            for p in found:
                grid_out[Point(dx, p.y)] = "#"
            dx += 1
        else:
            dx += 2
    return grid_out


def draw_grid(grid):
    w = max([p.x for p in grid.keys()]) + 1
    h = max([p.y for p in grid.keys()]) + 1
    for y in range(h):
        line = []
        for x in range(w):
            if grid.get(Point(x, y)):
                line.append("#")
            else:
                line.append(".")
        print("".join(line))


def solve1(entries):
    y = 0
    grid = {}
    for y, line in enumerate(entries):
        for x, c in enumerate(line):
            if c == "#":
                grid[Point(x, y)] = "#"
    draw_grid(grid)
    egrid = expand_cols(expand_rows(grid))
    print("Expanded:")
    draw_grid(egrid)
    stars = list(egrid.keys())
    print(stars)
    combinations = set(itertools.combinations(range(len(stars)), 2))
    print(combinations)
    print(len(combinations))
    distances = []
    for c in combinations:
        p1 = stars[c[0]]
        p2 = stars[c[1]]
        dist = abs(p1.x - p2.x) + abs(p1.y - p2.y)
        print(f"Distances between {c[0] + 1} and {c[1] + 1}: {dist}")
        distances.append(dist)
    return sum(distances)


def solve2(entries):
    pass


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 374)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), None)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
