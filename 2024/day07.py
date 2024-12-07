#!/usr/bin/env python3

# By Jakob Ruhe 2024-12-07

import os
import unittest
import sys
import itertools

# https://github.com/wimglenn/advent-of-code-data
# pip install advent-of-code-data
import aocd

# Local module
import utils


def parse_input(input):
    return [utils.parse_ints(e) for e in input.strip().split("\n")]


def eval(operands, operators):
    res = operands[0]
    for i, operator in enumerate(operators):
        operand = operands[i + 1]
        if operator == "+":
            res += operand
        elif operator == "*":
            res *= operand
        elif operator == "||":
            res = int(str(res) + str(operand))
        else:
            raise ValueError(operator)
    return res


def has_solution(numbers, available_operators):
    wanted = numbers[0]
    operands = numbers[1:]
    for p in itertools.product(available_operators, repeat=len(operands) - 1):
        if eval(operands, p) == wanted:
            return True
    return False


def solve_a(entries):
    return sum([e[0] if has_solution(e, ("+", "*")) else 0 for e in entries])


def solve_b(entries):
    return sum([e[0] if has_solution(e, ("+", "*", "||")) else 0 for e in entries])


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

    def test_a(self):
        self.assertEqual(solve_a(parse_input(self.input)), 3749)
        pass

    def test_b(self):
        self.assertEqual(solve_b(parse_input(self.input)), 11387)


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
