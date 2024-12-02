#!/usr/bin/env python3

# By Jakob Ruhe 2024-12-02

import os
import unittest
import sys

# https://github.com/wimglenn/advent-of-code-data
# pip install advent-of-code-data
import aocd

# Local module
import utils


def parse_input(input):
    return input.strip().split("\n")


def all_increasing(report):
    for a, b in zip(report, report[1:]):
        if b <= a:
            return False
    return True


def all_decreasing(report):
    for a, b in zip(report, report[1:]):
        if b >= a:
            return False
    return True


def ok_diff(report):
    for a, b in zip(report, report[1:]):
        diff = abs(a - b)
        if diff < 1 or diff > 3:
            return False
    return True


def is_safe(report):
    return ok_diff(report) and (all_increasing(report) or all_decreasing(report))


def solve_a(entries):
    reports = [utils.parse_ints(e) for e in entries]
    return sum([is_safe(report) for report in reports])


def solve_b(entries):
    num_safe = 0
    reports = [utils.parse_ints(e) for e in entries]
    for report in reports:
        if is_safe(report):
            num_safe += 1
            continue
        for i, _ in enumerate(report):
            clone = list(report)
            clone.pop(i)
            if is_safe(clone):
                num_safe += 1
                break
    return num_safe


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

    def test_a(self):
        self.assertEqual(solve_a(parse_input(self.input)), 2)

    def test_b(self):
        self.assertEqual(solve_b(parse_input(self.input)), 4)


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
