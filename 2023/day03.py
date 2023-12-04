#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-03

import os
import unittest
from collections import defaultdict
from utils import Point, all_adjacent


def parse_input(input):
    return input.strip().split("\n")


def has_number_neighbor_sym(location, grid):
    while grid.get(location, ".").isdigit():
        neighbors = all_adjacent(location)
        for nb in neighbors:
            c = grid.get(nb, ".")
            if c != "." and not c.isdigit():
                return True
        location = Point(location.x + 1, location.y)
    return False


def get_num(location, grid):
    num = []
    while grid.get(location, ".").isdigit():
        num.append(grid.get(location))
        location = Point(location.x + 1, location.y)
    return int("".join(num))


def solve1(entries):
    grid = {}
    for y, line in enumerate(entries):
        for x, c in enumerate(line.strip()):
            grid[Point(x, y)] = c
    sum = 0
    for y in range(len(entries)):
        for x in range(len(entries[0])):
            c = grid.get(Point(x, y), ".")
            if c.isdigit() and not grid.get(Point(x - 1, y), ".").isdigit():
                if has_number_neighbor_sym(Point(x, y), grid):
                    num = get_num(Point(x, y), grid)
                    sum += num
    return sum


def find_gears(start, grid):
    x, y = start
    gears = set()
    while grid.get(Point(x, y), ".").isdigit():
        neighbors = all_adjacent(Point(x, y))
        for nb in neighbors:
            c = grid.get(nb, ".")
            if c == "*":
                gears.add(nb)
        x += 1
    return gears


def solve2(entries):
    grid = {}
    for y, line in enumerate(entries):
        for x, c in enumerate(line.strip()):
            grid[(x, y)] = c
    all_gears = defaultdict(list)
    for y in range(len(entries)):
        for x in range(len(entries[0])):
            c = grid.get(Point(x, y), ".")
            if c.isdigit() and not grid.get(Point(x - 1, y), ".").isdigit():
                if gears := find_gears(Point(x, y), grid):
                    for g in gears:
                        all_gears[g].append(get_num(Point(x, y), grid))
    sum = 0
    for gear, numbers in all_gears.items():
        if len(numbers) == 2:
            sum += numbers[0] * numbers[1]
    return sum


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 4361)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 467835)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
