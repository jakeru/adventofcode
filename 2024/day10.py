#!/usr/bin/env python3

# By Jakob Ruhe 2024-12-10

import os
import unittest
import sys
from itertools import product

# https://github.com/wimglenn/advent-of-code-data
# pip install advent-of-code-data
import aocd

# Local module
from utils import walk, ORTHO_DIRS


def parse_input(input):
    indata = input.strip().split("\n")
    W = len(indata[0])
    H = len(indata)
    grid = {(x, y): int(indata[y][x]) for x, y in product(range(W), range(H))}
    trailheads = [pos for pos, height in grid.items() if height == 0]
    return grid, trailheads


def calc_score(grid, pos, visited, revisit):
    visited.add(pos)
    height = grid[pos]
    if height == 9:
        return 1
    total_score = 0
    for dir in ORTHO_DIRS:
        next_pos = walk(pos, dir)
        if grid.get(next_pos) == height + 1 and (revisit or next_pos not in visited):
            total_score += calc_score(grid, next_pos, visited, revisit)
    return total_score


def solve_a(grid, trailheads):
    return sum([calc_score(grid, th, set(), False) for th in trailheads])


def solve_b(grid, trailheads):
    return sum([calc_score(grid, th, set(), True) for th in trailheads])


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

    def test_a(self):
        self.assertEqual(solve_a(*parse_input(self.input)), 36)

    def test_b(self):
        self.assertEqual(solve_b(*parse_input(self.input)), 81)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        parsed_input = parse_input(f.read())

    parts = {
        "a": solve_a,
        "b": solve_b,
    }

    for part, solver in parts.items():
        submit = part in sys.argv
        answer = solver(*parsed_input)
        print(f"Answer of part {part}:")
        print(answer)
        if answer is not None and submit:
            aocd.submit(answer, part=part, reopen=False)
