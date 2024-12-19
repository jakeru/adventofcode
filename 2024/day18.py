#!/usr/bin/env python3

# By Jakob Ruhe 2024-12-18

import os
import unittest
import sys
import itertools

# https://github.com/wimglenn/advent-of-code-data
# pip install advent-of-code-data
import aocd

# Local module
from utils import parse_ints, walk, ORTHO_DIRS, djikstra


def parse_input(input):
    return [parse_ints(line) for line in input.strip().split("\n")]


def find_moves(nodes, state):
    return [(1, walk(state, dir)) for dir in ORTHO_DIRS if walk(state, dir) in nodes]


def solve_a(memory, steps=1024, maxxy=70):
    start = (0, 0)
    goal = (maxxy, maxxy)
    size = maxxy + 1

    all_nodes = set([(x, y) for x, y in itertools.product(range(size), range(size))])
    corrupted = set(memory[0:steps])
    nodes = all_nodes - corrupted

    return djikstra(nodes, find_moves, start, goal)


def can_reach_goal(nodes, start, goal):
    return djikstra(nodes, find_moves, start, goal) is not None


def solve_b(memory, maxxy=70):
    start = (0, 0)
    goal = (maxxy, maxxy)
    size = maxxy + 1

    all_nodes = set([(x, y) for x, y in itertools.product(range(size), range(size))])

    # Use Binary search to find the solution.
    # We want to find the first step at which we no longer can reach the goal.
    low = 1
    high = len(memory) - 1
    while high >= low:
        mid = (low + high) // 2
        print(f"At step {mid} {low=} {high=} last corrupted memory cell {memory[mid]}")
        if can_reach_goal(all_nodes - set(memory[0 : mid + 1]), start, goal):
            print(f"Could reach goal at step {mid}")
            low = mid + 1
        elif not can_reach_goal(all_nodes - set(memory[0:mid]), start, goal):
            print(f"Could not reach goal at step {mid} or previous step")
            high = mid - 1
        else:
            print(f"Could not reach goal at step {mid} but could at previous -> done")
            return ",".join(map(str, memory[mid]))


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""

    def test_a(self):
        self.assertEqual(solve_a(parse_input(self.input), 12, 6), 22)

    def test_b(self):
        self.assertEqual(solve_b(parse_input(self.input), 6), "6,1")


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
        answer = solver(parsed_input)
        print(f"Answer of part {part}:")
        print(answer)
        if answer is not None and submit:
            aocd.submit(answer, part=part, reopen=False)
