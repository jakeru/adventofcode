#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-19

import os
import re
import unittest


def parse_input(input):
    return input.strip().split("\n")


def is_accepted(workflows, part, current):
    while current != "A" and current != "R":
        w = workflows[current]
        next = w[-1][-1]
        for rule in w[:-1]:
            lhs, op, rhs, target = rule
            assert op in "<>"
            if part[lhs] < rhs if op == "<" else part[lhs] > rhs:
                next = target
                break
        current = next
    print(f"Part {part} ended up in {current}")
    return current == "A"


def solve1(entries):
    empty_line = entries.index("")

    # Parse workflows
    workflows = {}
    for line in entries[:empty_line]:
        m = re.match(r"(\S+){(\S+)}", line)
        assert m
        name, workflow = m[1], m[2].split(",")
        rules = []
        for w in workflow[:-1]:
            m = re.match(r"([xmas])([<>])(\d+):([a-zA-Z]+)", w)
            assert m
            lhs, op, rhs, target = m[1], m[2], m[3], m[4]
            rules.append((lhs, op, int(rhs), target))
        rules.append((None, None, None, workflow[-1]))
        workflows[name] = rules

    for name, w in workflows.items():
        print(f"W: {name} {w}")

    # Parse parts
    parts = []
    for line in entries[empty_line + 1 :]:
        ratings = re.findall(r"([xmas])=(\d+)", line)
        part = {}
        for r in ratings:
            part[r[0]] = int(r[1])
        parts.append(part)

    for p in parts:
        print(f"P: {p}")

    # Find accepted parts and take the sum of the ratings.
    accepted_parts = [p for p in parts if is_accepted(workflows, p, "in")]
    total = sum([sum(p.values()) for p in accepted_parts])

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
