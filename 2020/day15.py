#!/usr/bin/env python3

# By Jakob Ruhe 2020-12-15
#
# 06:51 p1 solved
# 07:12 p2 solved

import math
import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple

def parse_input(input):
    return input.strip()

def solve1(entries, turns):
    numbers = [int(e) for e in entries.split(",")]
    history = []
    for n in numbers:
        history.insert(0, n)
    for i in range(len(numbers), turns):
        last = history[0]
        try:
            spoken = history.index(last, 1)
        except ValueError:
            spoken = 0
        history.insert(0, spoken)
    return history[0]

def solve2(entries, turns):
    numbers = [int(e) for e in entries.split(",")]
    history_last = {}
    history_last_before_last = {}
    history_count = defaultdict(int)
    for i, n in enumerate(numbers):
        history_last[n] = i
        history_count[n] += 1
    last = numbers[-1]
    for i in range(len(numbers), turns):
        assert history_count[last] >= 1
        if history_count[last] == 1:
            spoken = 0
        else:
            spoken = history_last[last] - history_last_before_last[last]
        if spoken in history_count:
            history_last_before_last[spoken] = history_last[spoken]
        history_last[spoken] = i
        history_count[spoken] += 1
        last = spoken
    return last

# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    def test1(self):
        self.assertEqual(solve1("0,3,6", 2020), 436)
        self.assertEqual(solve1("1,3,2", 2020), 1)
        self.assertEqual(solve1("2,1,3", 2020), 10)
        self.assertEqual(solve1("1,2,3", 2020), 27)
    def test2(self):
        self.assertEqual(solve2("0,3,6", 2020), 436)
        self.assertEqual(solve2("1,3,2", 2020), 1)
        self.assertEqual(solve2("0,3,6", 30000000), 175594)
        self.assertEqual(solve2("1,3,2", 30000000), 2578)

if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(f"{solve1(entries, 2020)}")
    print(f"{solve2(entries, 30000000)}")
