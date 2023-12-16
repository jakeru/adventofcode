#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-16

import os
import unittest
from utils import Point, walk


def parse_input(input):
    return input.strip().split("\n")


def inside(pos, w, h):
    return pos.x >= 0 and pos.x < w and pos.y >= 0 and pos.y < h


def start_beam_at(grid, w, h, start, dir):
    energized = {}
    beams = [(start, dir)]
    while beams:
        beam = beams.pop()
        pos, dir = beam
        next_pos = walk(pos, dir)
        if not inside(next_pos, w, h):
            continue
        e = energized.get(next_pos)
        if e and dir in e:
            continue
        if e is None:
            energized[next_pos] = []
        energized[next_pos].append(dir)
        g = grid.get(next_pos)
        next_dir = None
        if g == "/":
            if dir == "E":
                next_dir = "N"
            elif dir == "S":
                next_dir = "W"
            elif dir == "W":
                next_dir = "S"
            elif dir == "N":
                next_dir = "E"
        elif g == "\\":
            if dir == "E":
                next_dir = "S"
            elif dir == "S":
                next_dir = "E"
            elif dir == "W":
                next_dir = "N"
            elif dir == "N":
                next_dir = "W"
        elif g == "-":
            if dir in "WE":
                next_dir = dir
            elif dir in "NS":
                beams.append((next_pos, "W"))
                beams.append((next_pos, "E"))
                continue
        elif g == "|":
            if dir in "WE":
                beams.append((next_pos, "N"))
                beams.append((next_pos, "S"))
                continue
            elif dir in "NS":
                next_dir = dir
        elif g is None:
            next_dir = dir
        assert next_dir is not None
        beams.append((next_pos, next_dir))
    return len(energized)


def parse_grid(entries):
    w = len(entries[0])
    h = len(entries)
    grid = {}
    for y, line in enumerate(reversed(entries)):
        for x, c in enumerate(line):
            if c != ".":
                grid[Point(x, y)] = c
    return grid, w, h


def solve1(entries):
    grid, w, h = parse_grid(entries)
    return start_beam_at(grid, w, h, Point(-1, h - 1), "E")


def solve2(entries):
    grid, w, h = parse_grid(entries)
    max_energized = 0
    for x in range(w):
        num1 = start_beam_at(grid, w, h, Point(x, -1), "N")
        num2 = start_beam_at(grid, w, h, Point(x, h), "S")
        max_energized = max(max_energized, num1, num2)
    for y in range(h):
        num1 = start_beam_at(grid, w, h, Point(-1, y), "E")
        num2 = start_beam_at(grid, w, h, Point(w, y), "W")
        max_energized = max(max_energized, num1, num2)
    return max_energized


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    def read_input(self):
        problem_name = os.path.splitext(os.path.basename(__file__))[0]
        with open(f"input/{problem_name}_testdata.txt") as f:
            return f.read()

    def test1(self):
        self.assertEqual(solve1(parse_input(self.read_input())), 46)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.read_input())), 51)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
