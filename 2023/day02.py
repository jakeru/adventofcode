#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-02

# Wrong: 2402
# Right: 2162

import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple
import utils

Show = namedtuple('Show', ['num', 'color'])

def parse_input(input):
    return input.strip().split("\n")

def parse_game(line):
    g1, g2 = line.split(':')
    print(g1, g2)
    subsets = g2.strip().split(';')
    print(subsets)
    subsets_out = []
    for subset in subsets:
        show_out = defaultdict(int)
        print(f"subset: {subset}")
        for show in subset.split(','):
            print(f"show: {show}")
            num, color = show.strip().split()
            show_out[color] += int(num)
        subsets_out.append(show_out)
    print(subsets_out)
    return subsets_out

def solve1(entries):
    possible = []
    for i, line in enumerate(entries):
        subsets = parse_game(line)
        subset_possible = True
        for subset in subsets:
            print(f'subset: {subset}')
            if subset.get('red', 0) > 12:
                subset_possible = False
            if subset.get('green', 0) > 13:
                subset_possible = False
            if subset.get('blue', 0) > 14:
                subset_possible = False
        print(f'{i + 1}: {subset_possible}')
        if subset_possible:
            possible.append(i + 1)
    return sum(possible)


def power_of_game(subsets):
    subset_min = defaultdict(int)
    for subset in subsets:
        subset_min['red'] = max(subset_min['red'], subset.get('red', 0))
        subset_min['green'] = max(subset_min['green'], subset.get('green', 0))
        subset_min['blue'] = max(subset_min['blue'], subset.get('blue', 0))
    return subset_min['red'] * subset_min['green'] * subset_min['blue']


def solve2(entries):
    power_sum = 0
    for i, line in enumerate(entries):
        subsets = parse_game(line)
        power = power_of_game(subsets)
        print(f'{i + 1}: {power}')
        power_sum += power
    return power_sum

# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 8)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 2286)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
