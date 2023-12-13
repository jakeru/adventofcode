#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-12

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
        groups = [int(w) for w in p2.split(',')]
        print(f"springs: {springs}")
        print(f"groups: {groups}")
        # total += num_arrangements(springs, groups)
        total += num_pos(0, springs, groups, {})
        unknowns = max(unknowns, len([c for c in springs if c == '?']))
    print(f"max unknowns: {unknowns} ({2**unknowns})")
    return total


def unfold_springs(springs):
    s = []
    for i in range(5):
        s.append(springs)
    return "?".join(s)

def unfold_groups(groups):
    return groups * 5

def num_pos(num_in_group, springs_left, groups_left, memo):
    if not springs_left:
        if len(groups_left) == 0 and num_in_group == 0:
            return 1
        elif len(groups_left) == 1 and num_in_group == groups_left[0]:
            return 1
        else:
            return 0
    if (springs_left, tuple(groups_left)) in memo:
        return memo[(springs_left, tuple(groups_left))]
    c = springs_left[0]
    if c == '#':
        return num_pos(num_in_group + 1, springs_left[1:], groups_left, memo)
    elif c == '.':
        if num_in_group > 0:
            if len(groups_left) >= 1 and groups_left[0] == num_in_group:
                return num_pos(0, springs_left[1:], groups_left[1:], memo)
            else:
                return 0
        else:
            res = num_pos(0, springs_left[1:], groups_left, memo)
            memo[(springs_left[1:], tuple(groups_left))] = res
            return res
    elif c == '?':
        u1 = num_pos(num_in_group, '#' + springs_left[1:], groups_left, memo)
        u2 = num_pos(num_in_group, '.' + springs_left[1:], groups_left, memo)
        return u1 + u2
    else:
        assert(False)

def solve2(entries):
    total = 0
    unknowns = 0
    for line in entries:
        springs, p2 = line.split()
        groups = [int(w) for w in p2.split(',')]
        print(f"springs: {springs}")
        springs_unfolded = unfold_springs(springs)
        print(f"springs unfolded: {springs_unfolded}")
        groups_unfolded = unfold_groups(groups)
        print(f"groups: {groups}")
        print(f"groups_unfolded: {groups_unfolded}")
        unknowns = max(unknowns, sum([1 for c in springs_unfolded if c == '?']))
        memo = {}
        num_arr = num_pos(0, springs_unfolded, groups_unfolded, memo)
        total += num_arr
        print(f"num_arr: {num_arr}")
    print(f"max unknowns: {unknowns} ({2**unknowns})")
    return total

# 49 in test data
# 94 unknowns in real input

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
        self.assertEqual(solve2(parse_input(self.input)), 525152)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
