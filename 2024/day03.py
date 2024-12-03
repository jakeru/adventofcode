#!/usr/bin/env python3

# By Jakob Ruhe 2024-12-03

import os
import re
import unittest
import sys

# https://github.com/wimglenn/advent-of-code-data
# pip install advent-of-code-data
import aocd


def parse_input(input):
    return input.strip()


def solve_a(entries):
    m = re.findall(r"mul\((\d+),(\d+)\)", entries)
    return sum([int(p[0]) * int(p[1]) for p in m])


def solve_b(entries):
    m = re.finditer(r"do\(\)|don't\(\)|mul\((\d+),(\d+)\)", entries)
    enable = True
    tot = 0
    for e in m:
        if e.group(0) == "do()":
            enable = True
        elif e.group(0) == "don't()":
            enable = False
        elif enable:
            tot += int(e.group(1)) * int(e.group(2))
    return tot


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input1 = """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""
    input2 = """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
    """

    def test_a(self):
        self.assertEqual(solve_a(parse_input(self.input1)), 161)

    def test_b(self):
        self.assertEqual(solve_b(parse_input(self.input2)), 48)


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
