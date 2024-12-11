#!/usr/bin/env python3

# By Jakob Ruhe 2024-12-11

import os
import unittest
import sys

# https://github.com/wimglenn/advent-of-code-data
# pip install advent-of-code-data
import aocd

# Local module
import utils


def parse_input(input):
    return input.strip().split("\n")


def step(stones):
    next = []
    for stone in stones:
        if stone == 0:
            next.append(1)
        elif len(str(stone)) % 2 == 0:
            L = len(str(stone)) // 2
            next.append(int(str(stone)[0:L]))
            next.append(int(str(stone)[L:]))
        else:
            next.append(stone * 2024)
    return next


def solve_a(indata):
    stones = utils.parse_ints(indata)
    for _ in range(25):
        stones = step(stones)
    return len(stones)


def num_stones(stone, steps, memory):
    if steps == 0:
        return 1
    elif (stone, steps) in memory:
        return memory[(stone, steps)]
    next = step([stone])
    tot = sum([num_stones(ns, steps - 1, memory) for ns in next])
    memory[(stone, steps)] = tot
    return tot


def solve_b(indata):
    stones = utils.parse_ints(indata)
    memory = {}
    return sum([num_stones(stone, 75, memory) for stone in stones])


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
125 17
"""

    def test_a(self):
        self.assertEqual(solve_a(*parse_input(self.input)), 55312)

    def test_b(self):
        self.assertEqual(solve_b(*parse_input(self.input)), 65601038650482)


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
