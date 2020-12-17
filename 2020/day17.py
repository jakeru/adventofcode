#!/usr/bin/env python3

# By Jakob Ruhe 2020-12-17
#
# 06:31 p1 solved
# 06:54 p2 solved

import math
import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple

def parse_input(input):
    return input.strip().split("\n")

def find_min_max(active, dims):
    min_ = [None] * dims
    max_ = [None] * dims
    for c in active:
        for i in range(dims):
            min_[i] = c[i] if min_[i] is None else min(min_[i], c[i])
            max_[i] = c[i] if max_[i] is None else max(max_[i], c[i])
    return min_, max_

def num_neighbors(coord, active):
    num = 0
    for z in range(0, 3):
        for y in range(0, 3):
            for x in range(0, 3):
                if x == 1 and y == 1 and z == 1:
                    continue
                if (coord[0] + x - 1, coord[1] + y - 1, coord[2] + z - 1) in active:
                    num += 1
    return num

def num_neighbors2(coord, active):
    num = 0
    for z in range(0, 3):
        for y in range(0, 3):
            for x in range(0, 3):
                for w in range(0, 3):
                    if w == 1 and x == 1 and y == 1 and z == 1:
                        continue
                    if (coord[0] + w - 1, coord[1] + x - 1, coord[2] + y - 1, coord[3] + z - 1) in active:
                        num += 1
    return num

# If a cube is active and exactly 2 or 3 of its neighbors are also active, the
# cube remains active. Otherwise, the cube becomes inactive. If a cube is
# inactive but exactly 3 of its neighbors are active, the cube becomes active.
# Otherwise, the cube remains inactive.

def simulate_step(active):
    next_active = set()
    min_, max_ = find_min_max(active, 3)
    for cz in range(min_[2] - 1, max_[2] + 2):
        for cy in range(min_[1] - 1, max_[1] + 2):
            for cx in range(min_[0] - 1, max_[0] + 2):
                neighbors = num_neighbors((cx, cy, cz), active)
                if (cx, cy, cz) in active:
                    if neighbors == 2 or neighbors == 3:
                        next_active.add((cx, cy, cz))
                elif neighbors == 3:
                    next_active.add((cx, cy, cz))
    return next_active

def simulate_step2(active):
    dims = 4
    next_active = set()
    min_, max_ = find_min_max(active, dims)
    for cz in range(min_[3] - 1, max_[3] + 2):
        for cy in range(min_[2] - 1, max_[2] + 2):
            for cx in range(min_[1] - 1, max_[1] + 2):
                for cw in range(min_[0] - 1, max_[0] + 2):
                    neighbors = num_neighbors2((cw, cx, cy, cz), active)
                    if (cw, cx, cy, cz) in active:
                        if neighbors == 2 or neighbors == 3:
                            next_active.add((cw, cx, cy, cz))
                    elif neighbors == 3:
                        next_active.add((cw, cx, cy, cz))
    return next_active

# How many cubes are left in the active state after the sixth cycle?
def solve1(entries):
    active = set()
    for y, row in enumerate(entries):
        for x, c in enumerate(row):
            print(x, y, c)
            if c == "#":
                active.add((x, y, 0))
    print("active", active)
    for step in range(6):
        active = simulate_step(active)
    return len(active)

def solve2(entries):
    print("P2", "*"*80)
    active = set()
    for y, row in enumerate(entries):
        for x, c in enumerate(row):
            print(x, y, c)
            if c == "#":
                active.add((0, x, y, 0))
    print("active", active)
    for step in range(6):
        active = simulate_step2(active)
    return len(active)

# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """.#.
..#
###
"""
    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 112)
    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 848)

if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print("P1", solve1(entries))
    print("P2", solve2(entries))
