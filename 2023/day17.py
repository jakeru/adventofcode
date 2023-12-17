#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-

import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple
import utils
from utils import Point, turn_left, turn_right, walk


def parse_input(input):
    return input.strip().split("\n")


def best_path(grid, start, goal, dir, num_steps_in_dir, memory):
    if start == goal:
        return 0
    if m := memory.get((start, dir, num_steps_in_dir)):
        return m
    costs = []
    l_dir = turn_left(dir)
    l_pos = walk(start, l_dir)
    if l_pos in grid:
        l_cost = best_path(grid, l_pos, goal, l_dir, 0, memory)
        costs.append(grid[l_pos] + l_cost)
    r_dir = turn_right(dir)
    r_pos = walk(start, r_dir)
    if r_pos in grid:
        r_cost = best_path(grid, r_pos, goal, r_dir, 0, memory)
        costs.append(grid[r_pos] + r_cost)
    f_pos = walk(start, dir)
    if f_pos in grid and num_steps_in_dir < 3:
        f_cost = best_path(grid, f_pos, goal, dir, num_steps_in_dir + 1, memory)
        costs.append(grid[f_pos] + f_cost)
    min_cost = min(costs)
    memory[(start, dir, num_steps_in_dir)] = min_cost
    return min_cost


def solve1(entries):
    grid = {}
    w = len(entries[0])
    h = len(entries)
    for y, line in enumerate(entries):
        for x, c in enumerate(line):
            grid[Point(x, y)] = int(c)
    memory = {}
    start = Point(0, h - 1)
    # start1 = Point(1, h - 1)
    # start2 = Point(0, h - 2)
    goal = Point(w - 1, 0)
#    c1 = best_path(grid, start1, goal, 'E', 1, memory)
#    c2 = best_path(grid, start2, goal, 'S', 1, memory)
#    return min(c1, c2)
    return best_path(grid, start, goal, 'E', -1, memory)

def solve2(entries):
    pass


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), None)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), None)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
