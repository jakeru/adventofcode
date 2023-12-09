#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-

import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple
import utils


def parse_input(input):
    return input.strip().split("\n")


def get_next(numbers):
    if all(n == 0 for n in numbers):
        return 0
    next_gen = []
    for i in range(1, len(numbers)):
        next_gen.append(numbers[i] - numbers[i-1])
    return numbers[-1] + get_next(next_gen)


def solve1(entries):
    total = 0
    for line in entries:
        numbers = [int(w) for w in line.split()]
        num = get_next(numbers)
        total += num
    return total


def solve2(entries):
    pass


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 114)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), None)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
