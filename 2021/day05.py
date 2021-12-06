#!/usr/bin/env python3

# By Jakob Ruhe 2021-12-05

# Note: This is not cleaned up after the problem got solved.

import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple
import utils

def parse_input(input):
    return input.strip().split("\n")

def is_horizontal(line):
    return line[0][1] == line[1][1]

def is_vertical(line):
    return line[0][0] == line[1][0]

def draw_line(line, squares):
    x1, y1 = line[0]
    x2, y2 = line[-1]
    dx = x2 - x1
    dy = y2 - y1
    x = x1
    y = y1
    while True:
        print(x, y)
        if (x, y) not in squares:
            squares[(x, y)] = 0
        squares[(x, y)] += 1
        if x == x2 and y == y2:
            break
        x += 1 if dx > 0 else (-1 if dx < 0 else 0)
        y += 1 if dy > 0 else (-1 if dy < 0 else 0)


def solve1(entries):
    lines = []
    for e in entries:
        coords = list(map(int, ",".join(e.split(" -> ")).split(",")))
        lines.append(((coords[0], coords[1]), (coords[2], coords[3])))
    print("lines", lines)
    squares = {}

    for line in lines:
        if is_horizontal(line) or is_vertical(line):
            print(line)
            draw_line(line, squares)

    for y in range(10):
        for x in range(10):
            if (x, y) in squares:
                print(squares[(x, y)], end="")
            else:
                print(".", end="")
        print()
    S = 0
    for s in squares.values():
        print(s)
        if s >= 2:
            S += 1
    return S



def solve2(entries):
    lines = []
    for e in entries:
        coords = list(map(int, ",".join(e.split(" -> ")).split(",")))
        lines.append(((coords[0], coords[1]), (coords[2], coords[3])))
    print("lines", lines)
    squares = {}

    for line in lines:
        draw_line(line, squares)

    for y in range(10):
        for x in range(10):
            if (x, y) in squares:
                print(squares[(x, y)], end="")
            else:
                print(".", end="")
        print()
    S = 0
    for s in squares.values():
        print(s)
        if s >= 2:
            S += 1
    return S

# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""
    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 5)
    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 12)

if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
