#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-08

import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple
import utils


def parse_input(input):
    return input.strip().split("\n")


def solve1(entries):
    dirs = entries[0]
    nodes = {}
    for line in entries[2:]:
        name, rest = line.split(' = ')
        left, right = rest.replace('(', '').replace(')', '').split(', ')
        print(f"{name}: left: {left}, right: {right}")
        nodes[name] = (left, right)
    dir_index = 0
    pos = "AAA"
    steps = 0
    while pos != 'ZZZ':
        d = 0 if dirs[dir_index] == 'L' else 1
        pos = nodes[pos][d]
        steps += 1
        dir_index = (dir_index + 1) % len(dirs)
    return steps


def solve2(entries):
    pass


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
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
