#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-19

import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple
import utils


def parse_input(input):
    return input.strip().split("\n")

def is_accepted(workflows, part, current):
    while current != 'A' and current != 'R':
        w = workflows[current]
        next = w[-1][-1]
        for rule in w[:-1]:
            lhs, op, rhs, target = rule
            if op == '<':
                if part[lhs] < rhs:
                    next = target
                    break
            elif op == '>':
                if part[lhs] > rhs:
                    next = target
                    break
            else:
                assert False
        print(f"Moving part from {current} to {next}")
        current = next
    print(f"Part {part} ended up in {current}")
    return current == 'A'


def solve1(entries):
    workflows = {}
    for line in entries:
        if not line:
            break
        print(line)
        # ([xmas])([<>])(\d+):([a-zA-Z]+)
        name, rest = line.replace('{', ' ').replace('}', '').split()
        rules = []
        workflow = rest.split(',')
        for w in workflow[:-1]:
            rule, target = w.split(':')
            op = '<' if '<' in rule else '>'
            lhs, rhs = rule.split(op)
            rules.append((lhs, op, int(rhs), target))
        rules.append((None, None, None, workflow[-1]))
        workflows[name] = rules
    for name, w in workflows.items():
        print(f"W: {name} {w}")

    parts = []
    empty_line = entries.index("")
    for line in entries[empty_line + 1:]:
        ratings = re.findall(r'([xmas])=(\d+)', line)
        part = {}
        for r in ratings:
            part[r[0]] = int(r[1])
        parts.append(part)

    for p in parts:
        print(f"P: {p}")

    accepted_parts = []
    for p in parts:
        if is_accepted(workflows, p, 'in'):
            accepted_parts.append(p)

    total = 0
    for p in accepted_parts:
        total += sum(p.values())

    return total


def solve2(entries):
    pass


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 19114)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), None)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
