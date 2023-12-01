#!/usr/bin/env python3

# By Jakob Ruhe 2022-12-22

import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple
import utils
from utils import Point, dir_from_name, dir_x, dir_y, turn_left, turn_right


Instr = namedtuple("Instr", ["count", "turn"])


def parse_input(input):
    return input


def parse_instr(instructions):
    groups = re.findall(r"(\d+)([RL])", instructions)
    return tuple([Instr(int(p[0]), p[1]) for p in groups])


def follow(grid, pos, direction, instr):
    for step in range(instr.count):
        nextp = Point(pos.x + dir_x(direction), pos.y + dir_y(direction))
        if not grid.get(nextp):
            if direction == dir_from_name("R"):
                next_x = min([p.x for p in grid if p.y == pos.y and grid.get(p)])
                nextp = Point(next_x, pos.y)
            elif direction == dir_from_name("L"):
                next_x = max([p.x for p in grid if p.y == pos.y and grid.get(p)])
                nextp = Point(next_x, pos.y)
            elif direction == dir_from_name("U"):
                next_y = max([p.y for p in grid if p.x == pos.x and grid.get(p)])
                nextp = Point(pos.x, next_y)
            elif direction == dir_from_name("D"):
                next_y = min([p.y for p in grid if p.x == pos.x and grid.get(p)])
                nextp = Point(pos.x, next_y)
        assert grid.get(nextp) in (".", "#")
        if grid.get(nextp) == ".":
            pos = nextp
    direction = turn_left(direction) if instr.turn == "L" else turn_right(direction)
    return pos, direction


def solve1(input):
    board, instr_str = input.split("\n\n")

    grid = {}
    wall = set()
    space = set()

    for y, line in enumerate(board.split("\n")):
        for x, v in enumerate(line):
            if v == ".":
                space.add(Point(x, y))
            elif v == "#":
                wall.add(Point(x, y))
            if v == "." or v == "#":
                grid[Point(x, y)] = v
            elif v != " ":
                raise ValueError(f"At ({x}, {y}): {v}")

    W = max([p.x for p in grid])
    H = max([p.y for p in grid])

    for y in range(W):
        row = []
        for x in range(H):
            row.append(grid.get(Point(x, y), " "))
        print("".join(row))

    instructions = parse_instr(instr_str)
    min_y = min([p.y for p in grid if grid[p] == "."])
    min_x = min([p.x for p in grid if grid[p] == "." and p.y == min_y])
    pos = Point(min_x, min_y)
    direction = dir_from_name("R")
    print(f"Start: {pos}")

    for instr in instructions:
        pos, direction = follow(grid, pos, direction, instr)
        print(f"At {pos} facing {direction} after {instr}")

    # 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^)

    d = (
        0
        if direction == dir_from_name("R")
        else 1
        if direction == dir_from_name("D")
        else 2
        if direction == dir_from_name("L")
        else 3
        if direction == dir_from_name("U")
        else None
    )

    return 1000 * (pos.y + 1) + 4 * (pos.x + 1) + d


def solve2(entries):
    pass


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""

    def test_instr(self):
        self.assertEqual(parse_instr("10R5L"), (Instr(10, "R"), Instr(5, "L")))

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 6032)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), None)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
