#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-18

import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple
import utils
from utils import Point, walk, ORTHO_DIRS


def parse_input(input):
    return input.strip().split("\n")


def print_grid(grid, inside_points):
    w = max([p.x for p in grid.keys()]) + 1
    h = max([p.y for p in grid.keys()]) + 1
    for y in range(h):
        line = []
        for x in range(w):
            if Point(x, y) in inside_points:
                line.append("i")
            else:
                c = grid.get(Point(x, y))
                line.append(c if c is not None else ".")
        print("".join(line))


def solve1(entries):
    instructions = []
    for line in entries:
        dir, dist, color = line.split()
        instructions.append((dir, int(dist), color))

    dir_map = {"U": "S", "D": "N", "L": "W", "R": "E"}

    grid = {}
    pos = Point(0, 0)
    for instr in instructions:
        dir, dist, _ = instr
        for _ in range(dist):
            grid[pos] = "#"
            pos = walk(pos, dir_map[dir])

    x_min = min([p.x for p in grid])
    y_min = min([p.y for p in grid])

    grid_moved = {}
    for p, c in grid.items():
        grid_moved[Point(p.x - x_min, p.y - y_min)] = c

    grid = grid_moved

    print_grid(grid, set())

    w = max([p.x for p in grid]) + 1
    h = max([p.y for p in grid]) + 1

    print("")

    # Let's hope the mid point is inside and flood fill from there.
    inside_points = set()
    first = Point(int(w / 2), int(h / 2))
    Q = []
    Q.append(first)
    while Q:
        node = Q.pop()
        assert node.x >= 0 and node.x < w and node.y >= 0 and node.y < h
        inside_points.add(node)
        around = []
        for dir in ORTHO_DIRS:
            around.append(walk(node, dir))
        for n in around:
            if grid.get(n) is None and n not in inside_points:
                Q.append(n)

    print_grid(grid, inside_points)

    return len(grid) + len(inside_points)


def solve2(entries):
    pass


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 62)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), None)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
