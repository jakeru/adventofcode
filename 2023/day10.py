#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-10

import os
import unittest
from utils import ORTHO_DIRS, Point, opposite_dir, walk


def parse_input(input):
    return input.strip().split("\n")


def find_connections(grid, pos):
    PIPES = {
        "|": set(("N", "S")),
        "-": set(("W", "E")),
        "L": set(("N", "E")),
        "J": set(("N", "W")),
        "7": set(("S", "W")),
        "F": set(("S", "E")),
        "S": set((ORTHO_DIRS)),
    }
    connections = []
    for dir in ORTHO_DIRS:
        if dir not in PIPES[grid[pos]]:
            continue
        pos2 = walk(pos, dir)
        if pos2 not in grid:
            continue
        if opposite_dir(dir) not in PIPES[grid[pos2]]:
            continue
        connections.append(pos2)
    return connections


def visit(grid, pos, dist, distances):
    if pos in distances:
        if distances[pos] <= dist:
            return []
    distances[pos] = dist
    connections = find_connections(grid, pos)
    assert len(connections) == 2
    return connections


def parse_grid(entries):
    grid = {}
    num_lines = len(entries)
    for y, line in enumerate(entries):
        for x, c in enumerate(line):
            if c != ".":
                grid[Point(x, num_lines - y)] = c
    return grid


def find_start(grid):
    for pos, pipe in grid.items():
        if pipe == "S":
            return pos


def find_loop(grid, start):
    distances = {}
    connections = visit(grid, start, 0, distances)
    dist = 1
    while connections:
        next_conn = []
        for conn in connections:
            next_conn.extend(visit(grid, conn, dist, distances))
        connections = next_conn
        dist += 1
    return distances


def solve1(entries):
    grid = parse_grid(entries)
    start = find_start(grid)
    loop = find_loop(grid, start)
    return max(loop.values())


def is_inside_loop(grid, loop, pos):
    # Walk from left to right until we reach `pos`.
    # Count number of crossings.
    # If number of crossings is an odd number `pos` is inside `loop`.
    crossed = []
    while pos.x >= 0:
        if pos in loop and grid.get(pos) in "|LJ7F":
            crossed.append(grid.get(pos))
        pos = walk(pos, "W")
    crossed = list(reversed(crossed))
    outside = True
    i = 0
    while i < len(crossed):
        c = crossed[i]
        nc = crossed[i + 1] if i < len(crossed) - 1 else None
        if c == "|":
            outside = not outside
        elif c == "L":
            if nc == "7":
                outside = not outside
            else:
                assert nc == "J"
            i += 1
        elif c == "F":
            if nc == "J":
                outside = not outside
            else:
                assert nc == "7"
            i += 1
        else:
            raise ValueError((c, nc))
        i += 1
    return not outside


def draw_grid(grid, w, h, loop, inside_loop):
    for y in range(h):
        line = []
        for x in range(w):
            pos = Point(x, h - y)
            if pos in inside_loop:
                line.append("I")
            elif pos in loop:
                line.append(grid.get(pos))
            else:
                line.append(".")
        print("".join(line))


def start_type(grid, start):
    c = find_connections(grid, start)
    n = walk(start, "N")
    s = walk(start, "S")
    w = walk(start, "W")
    e = walk(start, "E")
    if n in c and s in c:
        return "|"
    elif w in c and e in c:
        return "-"
    elif n in c and w in c:
        return "J"
    elif n in c and e in c:
        return "L"
    elif s in c and w in c:
        return "7"
    elif s in c and e in c:
        return "F"
    else:
        assert False


def solve2(entries):
    grid = parse_grid(entries)
    start = find_start(grid)
    loop = find_loop(grid, start)
    grid[start] = start_type(grid, start)
    print(f"Start: {start} {grid[start]}")
    w = max([p.x for p in grid.keys()]) + 1
    h = max([p.y for p in grid.keys()]) + 1
    inside_loop = set()
    for y in range(h):
        for x in range(w):
            pos = Point(x, y)
            if pos not in loop and is_inside_loop(grid, loop, pos):
                inside_loop.add(pos)
    draw_grid(grid, w, h, loop, inside_loop)
    return len(inside_loop)


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

    input3 = """
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""

    input4 = """
..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........
"""

    input5 = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""

    input6 = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
    """

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input1)), 4)
        self.assertEqual(solve1(parse_input(self.input2)), 8)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input3)), 4)
        self.assertEqual(solve2(parse_input(self.input4)), 4)
        self.assertEqual(solve2(parse_input(self.input5)), 8)
        self.assertEqual(solve2(parse_input(self.input6)), 10)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
