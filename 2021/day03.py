#!/usr/bin/env python3

# By Jakob Ruhe 2021-12-03

# Note: This is not cleaned up after the problem got solved.

import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple
import utils

def parse_input(input):
    return input.strip().split("\n")

def get_num_ones(entries):
    num_ones = [0] * len(entries[0])
    for e in entries:
        for i in range(len(e)):
            if e[i] == "1":
                num_ones[i] += 1
    return num_ones



def solve1(entries):
# power consumption
# produce
# gamma rate
# espilon rate
# power consumption = gamma rate * epsilon rate
    num_ones = [0] * len(entries[0])
    tot = len(entries)
    print(num_ones)
    for e in entries:
        for i in range(len(e)):
            if e[i] == "1":
                num_ones[i] += 1
    print(num_ones)
    ans = 0
    op = 0
    for e in num_ones:
        if e > tot / 2:
            ans = (ans << 1) | 0x01
            op = (op << 1)
        else:
            ans = (ans << 1)
            op = (op << 1) | 0x01
    print(ans, op)
    return ans * op

def oxygen(entries):
    left = entries.copy()
    print(left)
    for i in range(len(entries[0])):
        print("i", i)
        print("left", left)
        num_ones = get_num_ones(left)
        tot = len(left)
        print("num_ones", num_ones)
        print("tot", tot)
        keep = []
        num_ones_i = num_ones[i]
        num_zeroes_i = tot - num_ones[i]
        for num in left:
            if num_ones_i == num_zeroes_i and num[i] == "1":
                keep.append(num)
            elif num_zeroes_i < num_ones_i and num[i] == "1":
                keep.append(num)
            elif num_zeroes_i > num_ones_i and num[i] == "0":
                keep.append(num)
        left = keep
        if len(left) <= 1:
            break
    print("left", left)
    return left[0]

def scrubber_rating(entries):
    left = entries.copy()
    print(left)
    for i in range(len(entries[0])):
        print("i", i)
        print("left", left)
        num_ones = get_num_ones(left)
        tot = len(left)
        print("num_ones", num_ones)
        print("tot", tot)
        keep = []
        num_ones_i = num_ones[i]
        num_zeroes_i = tot - num_ones[i]
        for num in left:
            if num_ones_i == num_zeroes_i and num[i] == "0":
                keep.append(num)
            elif num_zeroes_i < num_ones_i and num[i] == "0":
                keep.append(num)
            elif num_zeroes_i > num_ones_i and num[i] == "1":
                keep.append(num)
        left = keep
        if len(left) <= 1:
            break
    print("left", left)
    return left[0]

def solve2(entries):
    # life supporting rating = oxygen generator rating * co2 scrubber rating
    #
    o = oxygen(entries)
    s = scrubber_rating(entries)
    return int(o, 2) * int(s, 2)


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""
    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 198)
    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 230)

if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
