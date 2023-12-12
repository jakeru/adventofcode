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

def build_config(springs, config):
    pos = 0
    springs_out = []
    for i, c in enumerate(springs):
        cc = c
        if cc == '?':
            cc = '.' if config & (1 << pos) else '#'
            pos += 1
        springs_out.append(cc)
    return "".join(springs_out)

def is_possible(springs, groups, config):
    num_damaged = 0
    damaged = []
    spring_config = build_config(springs, config)
    for c in spring_config:
        if c == '#':
            num_damaged += 1
        elif c == '.' and num_damaged > 0:
            damaged.append(num_damaged)
            num_damaged = 0
    if num_damaged > 0:
        damaged.append(num_damaged)
    #print(f"config {config} spring_config {spring_config} damaged {damaged}, possible: {damaged == groups}")
    return damaged == groups



def num_arrangements(springs, groups):
    # let all be off first
    num_possible = 0
    unknowns = len([c for c in springs if c == '?'])
    print(f"unknowns: {unknowns}")
    for i in range(2**unknowns):
        if is_possible(springs, groups, i):
            num_possible += 1
    return num_possible

def solve1(entries):
    total = 0
    unknowns = 0
    for line in entries:
        springs, p2 = line.split()
        # springs = [c for c in p1]
        groups = [int(w) for w in p2.split(',')]
        print(f"springs: {springs}")
        print(f"groups: {groups}")
        total += num_arrangements(springs, groups)
        unknowns = max(unknowns, len([c for c in springs if c == '?']))
    print(f"max unknowns: {unknowns} ({2**unknowns})")
    return total


def solve2(entries):
    pass


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 21)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), None)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
