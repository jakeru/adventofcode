#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-01

import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple
import utils


def parse_input(input):
    return input.strip().split("\n")


def solve1(entries):
    s = 0
    for line in entries:
        print(line)
        digits = []
        for c in line:
            if c.isdigit():
                digits.append(c)
        print(digits)
        s += int("".join([digits[0], digits[-1]]))
    return s

# wrong: 17790
# wrong: 17829
# wrong: 17785

def solve2(entries):
    words = {"one": 1,
             "two": 2,
             "three": 3,
             "four": 4,
             "five": 5,
             "six": 6,
             "seven": 7,
             "eight": 8,
             "nine": 9}
    s = 0
    for line in entries:
        print(line)
        digits = []
        digits_pos = []
        for i, c in enumerate(line):
            if c.isdigit():
                digits.append(c)
                digits_pos.append(i)
        print(digits)
        w1pos = None
        w1 = None
        for w in words.keys():
            pos = line.find(w)
            if pos >= 0 and (w1pos is None or pos < w1pos):
                w1pos = pos
                w1 = w
        w2pos = None
        w2 = None
        for w in words.keys():
            pos = line.rfind(w)
            if pos >= 0 and (w2pos is None or pos > w2pos):
                w2pos = pos
                w2 = w
        d1 = digits[0]
        if w1pos is not None and w1pos < digits_pos[0]:
            d1 = str(words[w1])
        d2 = digits[-1]
        if w2pos is not None and w2pos > digits_pos[-1]:
            d2 = str(words[w2])
        print(f"w {w1} {w1pos} {w2} {w2pos}")
        print(d1, d2)
        s += int("".join([d1, d2]))
    return s


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
    # print(solve1(entries))
    print(solve2(entries))
