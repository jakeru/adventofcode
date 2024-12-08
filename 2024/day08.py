#!/usr/bin/env python3

# By Jakob Ruhe 2024-12-08 (later at the day instead of the morning)

import os
import unittest
import sys
from collections import defaultdict
from itertools import permutations

# https://github.com/wimglenn/advent-of-code-data
# pip install advent-of-code-data
import aocd

# Local module
import utils


def parse_input(input):
    lines = input.strip().split("\n")
    W = len(lines[0])
    H = len(lines)
    antennas = defaultdict(list)
    for y in range(H):
        for x in range(W):
            c = lines[y][x]
            if c != ".":
                antennas[c].append((x, y))
    return antennas, W, H


def is_double_distance(p1, p2, p3):
    d1 = utils.sqdist(p1, p2)
    d2 = utils.sqdist(p1, p3)
    return d1 == d2 * 4 or d2 == d1 * 4


def is_any_distance(p1, p2, p3):
    return True


def find_antinodes(antennas, W, H, distance_cond):
    antinodes = set()

    for y in range(H):
        for x in range(W):
            for id in antennas:
                for pair in permutations(antennas[id], 2):
                    if not utils.colinear((x, y), pair[0], pair[1]):
                        continue
                    if not distance_cond((x, y), pair[0], pair[1]):
                        continue
                    antinodes.add((x, y))
                    break

    return antinodes


def solve_a(antennas, W, H):
    return len(find_antinodes(antennas, W, H, is_double_distance))


def solve_b(antennas, W, H):
    return len(find_antinodes(antennas, W, H, is_any_distance))


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

    def test_a(self):
        self.assertEqual(solve_a(*parse_input(self.input)), 14)

    def test_b(self):
        self.assertEqual(solve_b(*parse_input(self.input)), 34)


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
        answer = solver(*entries)
        print(f"Answer of part {part}:")
        print(answer)
        if answer is not None and submit:
            aocd.submit(answer, part=part, reopen=False)
