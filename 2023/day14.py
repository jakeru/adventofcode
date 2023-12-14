#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-14

import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple
import utils
from utils import Point


def parse_input(input):
    return input.strip().split("\n")


def print_rocks(rocks, w, h):
    for y in range(w):
        line = []
        for x in range(h):
            r = rocks.get(Point(x, y))
            line.append(r if r is not None else '.')
        print("".join(line))

def move_rock_north(rocks, pos):
    r = rocks.pop(pos)
    while pos.y > 0 and rocks.get(Point(pos.x, pos.y - 1)) is None:
        pos = Point(pos.x, pos.y - 1)
    rocks[pos] = r


def solve1(entries):
    rocks = {}
    for y, line in enumerate(entries):
        for x, c in enumerate(line):
            if c != '.':
                rocks[Point(x, y)] = c
    w = max([p.x for p in rocks]) + 1
    h = max([p.y for p in rocks]) + 1

    print_rocks(rocks, w, h)

    # for x in range(w):
    #     for y in range(h):
    #         r = rocks.get(Point(x, y))
    #         if r == 'O':
    #             move_rock_north(rocks, Point(x, y))
    move_rocks_north(rocks, w, h)

    print_rocks(rocks, w, h)

    total = 0
    for pos, r in rocks.items():
        if r == 'O':
            total += h - pos.y

    return total

def move_rocks_north(rocks, w, h):
    for x in range(w):
        new_pos = 0
        for y in range(h):
            r = rocks.get(Point(x, y))
            if r == 'O':
                if new_pos < y:
                    rocks.pop(Point(x, y))
                    rocks[Point(x, new_pos)] = r
                    new_pos = new_pos + 1
                else:
                    new_pos = y + 1
            elif r == '#':
                new_pos = y + 1

def move_rocks_south(rocks, w, h):
    for x in range(w):
        new_pos = h - 1
        for y in range(h - 1, -1, -1):
            r = rocks.get(Point(x, y))
            if r == 'O':
                if new_pos > y:
                    rocks.pop(Point(x, y))
                    rocks[Point(x, new_pos)] = r
                    new_pos = new_pos - 1
                else:
                    new_pos = y - 1
            elif r == '#':
                new_pos = y - 1

def move_rocks_west(rocks, w, h):
    for y in range(h):
        new_pos = 0
        for x in range(w):
            r = rocks.get(Point(x, y))
            if r == 'O':
                if new_pos < x:
                    rocks.pop(Point(x, y))
                    rocks[Point(new_pos, y)] = r
                    new_pos = new_pos + 1
                else:
                    new_pos = x + 1
            elif r == '#':
                new_pos = x + 1

def move_rocks_east(rocks, w, h):
    for y in range(h):
        new_pos = w - 1
        for x in range(w - 1, -1, -1):
            r = rocks.get(Point(x, y))
            if r == 'O':
                if new_pos > x:
                    rocks.pop(Point(x, y))
                    rocks[Point(new_pos, y)] = r
                    new_pos = new_pos - 1
                else:
                    new_pos = x - 1
            elif r == '#':
                new_pos = x - 1


def calc_load(rocks, h):
    total = 0
    for pos, r in rocks.items():
        if r == 'O':
            total += h - pos.y
    return total

def solve2(entries):
    rocks = {}
    for y, line in enumerate(entries):
        for x, c in enumerate(line):
            if c != '.':
                rocks[Point(x, y)] = c

    w = max([p.x for p in rocks]) + 1
    h = max([p.y for p in rocks]) + 1

    print("Initial:")
    print_rocks(rocks, w, h)

    memory = {}
    memory[0] = calc_load(rocks, h)

    mem = {}
    repeats_after_cycle = None
    repeats_to = None

    for cycle in range(1000):
        move_rocks_north(rocks, w, h)
        move_rocks_west(rocks, w, h)
        move_rocks_south(rocks, w, h)
        move_rocks_east(rocks, w, h)
        load = calc_load(rocks, h)
        memory[cycle+1] = load
        print(f"After cycle {cycle + 1}, load: {load}")
        id = hash(frozenset(rocks.items()))
        if id in mem:
            print(f"After cycle {cycle+1} Found same id at cycle {mem[id]}")
            repeats_after_cycle = cycle + 1
            repeats_to = mem[id]
            break
        else:
            mem[id] = cycle + 1

        # print_rocks(rocks, w, h)

    # After cycle 160 Found same at id at cycle 94
    print(f"repeats_after_cycle: {repeats_after_cycle}")
    print(f"repeats_to: {repeats_to}")
    cycle = repeats_to
    T = repeats_after_cycle - repeats_to

    for num in range(10, 100):
        look = (num - repeats_to) % T + repeats_to
        print(f"For num {num} Looking at: {look}")

    num = 1000000000
    look = (num - repeats_to) % T + repeats_to
    print(f"For num {num} Looking at: {look}")

    return memory[look]


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 136)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 64)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
