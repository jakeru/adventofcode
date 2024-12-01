#!/usr/bin/env python3

# By Jakob Ruhe 2024-12-dd

import os
import re
import unittest
import sys
from collections import defaultdict
from collections import namedtuple
import utils
import aocd


def parse_input(input):
    return input.strip().split("\n")


def solve_a(entries):
    pass


def solve_b(entries):
    pass


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
"""

    def test_a(self):
        self.assertEqual(solve_a(parse_input(self.input)), None)

    def test_b(self):
        self.assertEqual(solve_b(parse_input(self.input)), None)


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
