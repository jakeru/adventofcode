#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-04

import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple
import utils


def parse_input(input):
    return input.strip().split("\n")


# Wrong: 8320
# Wrong: 55508

def solve1(entries):
    total = 0
    for line in entries:
        w, c = line.split('|')
        _, w = w.split(':')
        winning = utils.parse_ints(w)
        cards = utils.parse_ints(c)
        print(f'winning {winning}')
        print(f'cards {cards}')
        points = 0
        p = 1
        num_won = 0
        for c in cards:
            if c in winning:
                num_won += 1
                points += p
                p *= 2
                print(f"card {c} match")
        # total += points
        if num_won > 0:
            total += 2 ** (num_won - 1)
            print(f"{num_won} wins gives {2 ** num_won} points")
    return total


def solve2(entries):
    pass


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 13)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), None)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
