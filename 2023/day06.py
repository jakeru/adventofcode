#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-

import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple
import utils
import math


def parse_input(input):
    return input.strip().split("\n")


def num_ways_to_win(total_time, min_dist):
    distances = []
    for t in range(total_time):
        distance = t * (total_time - t)
        distances.append(distance)
    return len(tuple(d for d in distances if d > min_dist))


def solve1(entries):
    times = tuple(int(w) for w in entries[0].split(':')[1].split())
    distances = tuple(int(w) for w in entries[1].split(':')[1].split())
    print(f"times {times}")
    print(f"distances {distances}")
    num_ways = []
    for i, t in enumerate(times):
        num_ways.append(num_ways_to_win(t, distances[i]))
    return math.prod(num_ways)


def solve2(entries):
    pass


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
Time:      7  15   30
Distance:  9  40  200
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
