#!/usr/bin/env python3

# By Jakob Ruhe 2024-12-05

import os
import unittest
import sys

# https://github.com/wimglenn/advent-of-code-data
# pip install advent-of-code-data
import aocd

# Local module
import utils


def parse_input(input):
    return input.strip()


def parse_rules_and_produce_list(input):
    p1, p2 = input.strip().split("\n\n")

    rules = []
    for line in p1.split("\n"):
        a, b = line.split("|")
        rules.append((int(a), int(b)))

    produce_list = []
    for line in p2.split("\n"):
        produce_list.append(utils.parse_ints(line))

    return (rules, produce_list)


def is_valid(p, rules):
    for r in rules:
        try:
            if p.index(r[0]) > p.index(r[1]):
                return False
        except ValueError:
            continue
    return True


def fix_list(p, rules):
    clone = list(p)
    while not is_valid(clone, rules):
        swapped = False
        for r in rules:
            a = r[0]
            b = r[1]
            try:
                pos_a = clone.index(a)
                pos_b = clone.index(b)
                if pos_a > pos_b:
                    clone[pos_a], clone[pos_b] = clone[pos_b], clone[pos_a]
                    swapped = True
            except ValueError:
                pass
        assert swapped
    return clone


def solve_a(input):
    rules, produce_list = parse_rules_and_produce_list(input)

    # Make sure rules are fair.
    for r in rules:
        assert r[0] != r[1]

    # Make sure pages in produce lists are unique.
    for p in produce_list:
        assert len(p) == len(set(p))

    # Find valid rules.
    tot = 0
    for p in produce_list:
        if not is_valid(p, rules):
            continue
        assert len(p) % 2 == 1
        tot += p[len(p) // 2]

    return tot


def solve_b(input):
    rules, produce_list = parse_rules_and_produce_list(input)

    # Fix invalid rules.
    tot = 0
    for p in produce_list:
        if is_valid(p, rules):
            continue
        fixed = fix_list(p, rules)
        assert sorted(p) == sorted(fixed)
        assert len(fixed) % 2 == 1
        tot += fixed[len(fixed) // 2]

    return tot


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

    def test_a(self):
        self.assertEqual(solve_a(parse_input(self.input)), 143)

    def test_b(self):
        self.assertEqual(solve_b(parse_input(self.input)), 123)


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
