#!/usr/bin/env python3

# By Jakob Ruhe 2024-12-01

import os
import unittest
import sys
import utils
import aocd


def parse_input(input):
    return input.strip().split("\n")


def solve_a(entries):
    numbers = [utils.parse_ints(e) for e in entries]
    a = sorted([e[0] for e in numbers])
    b = sorted([e[1] for e in numbers])
    diffs = [abs(aa - bb) for (aa, bb) in zip(a, b)]
    return sum(diffs)


def solve_b(entries):
    numbers = [utils.parse_ints(e) for e in entries]
    a = [e[0] for e in numbers]
    b = [e[1] for e in numbers]
    prods = []
    for aa in a:
        num = sum(int(aa == bb) for bb in b)
        prods.append(aa * num)
    return sum(prods)


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
3   4
4   3
2   5
1   3
3   9
3   3
"""

    def test_a(self):
        self.assertEqual(solve_a(parse_input(self.input)), 11)

    def test_b(self):
        self.assertEqual(solve_b(parse_input(self.input)), 31)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())

    parts = {
        "a": solve_a,
        "b": solve_b,
    }

    for part, solver in parts.items():
        submit = part in sys.argv
        answer = solver(entries)
        print(f"Answer of part {part}:")
        print(answer)
        if answer is not None and submit:
            aocd.submit(answer, part=part, reopen=False)
