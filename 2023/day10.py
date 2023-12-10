#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-10

import os
import unittest
from utils import ORTHO_DIRS, Point, dir_x, dir_y, opposite_dir

pipes = {
    "|": set(("N", "S")),
    "-": set(("W", "E")),
    "L": set(("N", "E")),
    "J": set(("N", "W")),
    "7": set(("S", "W")),
    "F": set(("S", "E")),
    "S": set((ORTHO_DIRS)),
}


def parse_input(input):
    return input.strip().split("\n")


def find_connections(grid, pos):
    connections = []
    for dir in ORTHO_DIRS:
        if dir not in pipes[grid[pos]]:
            continue
        pos2 = Point(pos.x + dir_x(dir), pos.y + dir_y(dir))
        if pos2 not in grid:
            continue
        if opposite_dir(dir) not in pipes[grid[pos2]]:
            continue
        connections.append(pos2)
    return connections


def visit(grid, pos, dist, distances):
    print(f"visit {pos} {grid[pos]} dist {dist}")
    if pos in distances:
        if distances[pos] <= dist:
            print(
                f"visit {pos} {grid[pos]} dist {dist}: already have better {distances[pos]}"
            )
            return []
    distances[pos] = dist
    connections = find_connections(grid, pos)
    print(f"visit {pos} found connections: {connections}")
    return connections


def solve1(entries):
    grid = {}
    start = None
    num_lines = len(entries)
    for y, line in enumerate(entries):
        for x, c in enumerate(line):
            if c != ".":
                grid[Point(x, num_lines - y)] = c
    for pos, pipe in grid.items():
        if pipe == "S":
            start = pos
            break
    print(f"Start: {start}")
    distances = {}
    connections = visit(grid, start, 0, distances)
    dist = 1
    while connections:
        next_conn = []
        for conn in connections:
            next_conn.extend(visit(grid, conn, dist, distances))
        connections = next_conn
        dist += 1
    return max(distances.values())


def solve2(entries):
    pass


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input1 = """
.....
.S-7.
.|.|.
.L-J.
.....
"""

    input2 = """
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input1)), 4)
        self.assertEqual(solve1(parse_input(self.input2)), 8)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input1)), None)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
