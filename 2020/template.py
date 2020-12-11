#!/usr/bin/env python3

# By Jakob Ruhe 2020-12-

import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple

def parse_input(input):
    return input.strip().split("\n")

def solve1(entries):
    pass

def solve2(entries):
    pass

# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
"""
    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), None)
    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), None)

if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(f"{solve1(entries)}")
    print(f"{solve2(entries)}")
