#!/usr/bin/env python3

# By Jakob Ruhe 2024-12-04

import os
import unittest
import sys

# https://github.com/wimglenn/advent-of-code-data
# pip install advent-of-code-data
import aocd


def parse_input(input):
    return input.strip().split("\n")


def num_times_in(text):
    return sum([text[start:].startswith("XMAS") for start, _ in enumerate(text)])


def build_grid(entries):
    grid = {}
    for y in range(S):
        for x in range(S):
            grid[(x, y)] = entries[y][x]
    return grid


def solve_a(entries):
    S = len(entries)
    assert S == len(entries[0])

    grid = build_grid(entries)

    lines = []

    # Horisontal
    for y in range(S):
        w = [grid[(x, y)] for x in range(S)]
        lines.append("".join(w))

    # Vertical
    for x in range(S):
        w = [grid[(x, y)] for y in range(S)]
        lines.append("".join(w))

    # Diagonal starting on x = 0, y = 0..S, going down right.
    for sy in range(S):
        w = [grid[(i, sy + i)] for i in range(S - sy)]
        lines.append("".join(w))

    # Diagonal starting on x = 1..S, y = 0, going down right.
    for sx in range(1, S):
        w = [grid[(sx + i, i)] for i in range(S - sx)]
        lines.append("".join(w))

    # Diagonal starting on x = 0, y = 0..S, going up right.
    for sy in range(S):
        w = [grid[(i, sy - i)] for i in range(sy + 1)]
        lines.append("".join(w))

    # Diagonal starting on x = 1..S, y = S-1, going up right.
    for sx in range(1, S):
        w = [grid[(sx + i, S - 1 - i)] for i in range(S - sx)]
        lines.append("".join(w))

    return sum([num_times_in(line) + num_times_in(line[::-1]) for line in lines])


def solve_b(entries):
    S = len(entries)
    assert S == len(entries[0])

    grid = build_grid(entries)

    total = 0
    for sy in range(S):
        for sx in range(S):
            if grid.get((sx, sy)) != "A":
                continue
            w1 = grid.get((sx - 1, sy - 1)) == "M" and grid.get((sx + 1, sy + 1)) == "S"
            w2 = grid.get((sx - 1, sy - 1)) == "S" and grid.get((sx + 1, sy + 1)) == "M"
            w3 = grid.get((sx - 1, sy + 1)) == "M" and grid.get((sx + 1, sy - 1)) == "S"
            w4 = grid.get((sx - 1, sy + 1)) == "S" and grid.get((sx + 1, sy - 1)) == "M"
            if (w1 or w2) and (w3 or w4):
                total += 1
    return total


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input_a = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

    input_b = """
.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
"""

    def test_a(self):
        self.assertEqual(num_times_in("_XMAS_XMAS_"), 2)
        self.assertEqual(solve_a(parse_input(self.input_a)), 18)

    def test_b(self):
        self.assertEqual(solve_b(parse_input(self.input_b)), 9)


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
