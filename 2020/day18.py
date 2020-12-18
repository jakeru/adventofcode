#!/usr/bin/env python3

# By Jakob Ruhe 2020-12-18

import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple

def parse_input(input):
    return input.strip().split("\n")

def eval_expr(tokens):
    if len(tokens) == 1:
        return int(tokens[0])
    if tokens[-1] == ")":
        num = 1
        i = -1
        while num >= 0:
            if tokens[i] == ")":
                num += 1

    else:
        rhs = int(tokens[-1])
    op = tokens[-2]
    lhs = eval_expr(tokens[0:-2])
    if op == "+":
        return lhs + rhs
    elif op == "-":
        return lhs - rhs
    elif op == "*":
        return lhs * rhs
    else:
        raise ValueError(f"Unknown op: {op}")

def calc(expr):
    print("Expression", expr)
    tokens = expr.replace("(", " ( ").replace(")", " ) ").strip().split()
    print("tokens", tokens)
    return eval_expr(tokens)

def solve1(entries):
    sum_ = 0
    for e in entries:
        sum_ += calc(e)
    return sum_

def solve2(entries):
    pass

# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """1 + 2 * 3 + 4 * 5 + 6
"""
    input2 = """((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""
    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 71)
        self.assertEqual(solve1(parse_input(self.input2)), 13632)
    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), None)

if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(f"{solve1(entries)}")
    print(f"{solve2(entries)}")
