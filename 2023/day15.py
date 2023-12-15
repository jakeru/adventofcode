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


def calc_hash(string):
    h = 0
    for c in string:
        h += ord(c)
        h *= 17
        h = h % 256
    return h

# Wrong: 92934

def solve1(entries):
    total = 0
    for line in entries:
        tokens = line.split(',')
        for t in tokens:
            h = calc_hash(t)
            print(f"hash of '{t}' is {h}")
            total += h
    return total


def solve2(entries):
    pass


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
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
