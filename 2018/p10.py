#!/usr/bin/env python3

# By Jakob Ruhe 2018-12-10

import unittest
import collections
import re
from functools import reduce

Point = collections.namedtuple('Point', ['x', 'y'])

class Star:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

def parse_star(str):
    m = re.match(r"position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>", str)
    args = map(lambda i: int(m.group(i)), range(1, 5))
    return Star(*args)

def next(stars, time):
    for star in stars:
        star.x += star.vx
        star.y += star.vy
    return time + 1

def prev(stars, time):
    for star in stars:
        star.x -= star.vx
        star.y -= star.vy
    return time - 1

def get_min(stars):
    return Point(
        min(stars, key=lambda star: star.x).x,
        min(stars, key=lambda star: star.y).y
    )

def get_max(stars):
    return Point(
        max(stars, key=lambda star: star.x).x,
        max(stars, key=lambda star: star.y).y
    )

def print_stars(stars, time):
    min_point = get_min(stars)
    max_point = get_max(stars)
    width = max_point.x - min_point.x
    height = max_point.y - min_point.y
    print("Time: {}".format(time))
    rows = []
    for y in range(0, height + 1):
        rows.append(["."] * (width + 1))
    for s in stars:
        rows[s.y - min_point.y][s.x - min_point.x] = "#"
    for row in rows:
        print("".join(row))

def solve(file):
    with open(file, "r") as f:
        stars = list(map(lambda line: parse_star(line), f.readlines()))
    print("Number of stars: {}".format(len(stars)))
    time = 0
    prev_width = None
    prev_height = None
    # Idea of solution:
    # Loop until the universe gets bigger.
    # When that happens, back time 2 seconds and print a couple of frames.
    while True:
        min_point = get_min(stars)
        max_point = get_max(stars)
        width = max_point.x - min_point.x
        height = max_point.y - min_point.y
        if time > 0:
            if prev_width < width or prev_height < height:
                break
        prev_width = width
        prev_height = height
        time = next(stars, time)
    print("Stopped at: {}".format(time))
    print("width: {}, height: {}".format(width, height))
    print("min: {}".format(min_point))
    time = prev(stars, time)
    time = prev(stars, time)
    print_stars(stars, time)
    time = next(stars, time)
    print_stars(stars, time)
    time = next(stars, time)
    print_stars(stars, time)
    time = next(stars, time)
    print_stars(stars, time)

class TestThis(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(
            parse_star("position=< 31650, -41911> velocity=<-3,  4>"),
            Star(31650, -41911, -3, 4))
        self.assertEqual(
            parse_star("position=< 6,  10> velocity=<-2, -1>"),
            Star(6, 10, -2, -1))
    def test_solve(self):
        solve("p10_testdata.txt")

if __name__ == "__main__":
    #unittest.main()
    solve("p10/p10_input.txt")
