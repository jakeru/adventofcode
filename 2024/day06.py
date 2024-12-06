#!/usr/bin/env python3

# By Jakob Ruhe 2024-12-dd

import os
import re
import unittest
import sys
from collections import defaultdict
from collections import namedtuple

# https://github.com/wimglenn/advent-of-code-data
# pip install advent-of-code-data
import aocd

# Local module
import utils
from utils import Point, walk, turn, ORTHO_DIRS


def parse_input(input):
    return input.strip().split("\n")


def parse(entries):
    guard_pos = None
    guard_dir = None
    dirs = "^<v^"
    obstacles = set()
    floor = set()
    for y, entry in enumerate(entries):
        for x, s in enumerate(entry):
            if s == "#":
                obstacles.add((x, y))
            elif s in dirs:
                guard_pos = Point(x, y)
                guard_dir = ORTHO_DIRS[dirs.index(s)]
                floor.add((x, y))
            elif s == ".":
                floor.add((x, y))
            else:
                raise ValueError((x, y, s))
    return guard_pos, guard_dir, obstacles, floor


def solve_a(entries):
    guard_pos, guard_dir, obstacles, floor = parse(entries)

    W = len(entries[0])
    H = len(entries)
    print(f"{W=}")
    print(f"{H=}")
    print(f"{guard_dir=}")
    print(f"{guard_pos=}")
    for y in range(H):
        row = []
        for x in range(W):
            if (x, y) in obstacles:
                row.append("#")
            else:
                row.append(".")
        print("".join(row))

    visited = set()
    while True:
        visited.add(guard_pos)
        print(f"{guard_dir=}")
        print(f"{guard_pos=}")
        next = walk(guard_pos, guard_dir)
        if next in obstacles:
            guard_dir = turn(guard_dir, -2)
        elif next in floor:
            guard_pos = next
        else:
            break
    return len(visited)


def will_create_loop(guard_pos, guard_dir, obstacles, floor):
    visited = set()
    visited_dir = set()
    while True:
        visited.add(guard_pos)
        visited_dir.add((guard_pos, guard_dir))
        next = walk(guard_pos, guard_dir)
        if next in obstacles:
            guard_dir = turn(guard_dir, -2)
        elif next in floor:
            guard_pos = next
        else:
            break
        if (guard_pos, guard_dir) in visited_dir:
            return True
    return False


def solve_b(entries):
    guard_pos, guard_dir, obstacles, floor = parse(entries)
    W = len(entries[0])
    H = len(entries)
    loops = []
    for y in range(H):
        for x in range(W):
            if (x, y) in obstacles or guard_pos == Point(x, y):
                continue
            o = obstacles | set([(x, y)])
            if will_create_loop(guard_pos, guard_dir, o, floor):
                loops.append((x, y))
    return len(loops)


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

    def test_a(self):
        self.assertEqual(solve_a(parse_input(self.input)), 41)

    def test_b(self):
        self.assertEqual(solve_b(parse_input(self.input)), 6)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())

    parts = {
        "a": solve_a,
        "b": solve_b,
    }

    for part, solver in parts.items():
        submit = part in sys.argv
        answer = solver(entries)
        print(f"Answer of part {part}:")
        print(answer)
        if answer is not None and submit:
            aocd.submit(answer, part=part, reopen=False)
