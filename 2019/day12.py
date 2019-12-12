#!/usr/bin/env python3

# By Jakob Ruhe 2019-12-12
# Started at 06:37

import unittest
import re
from collections import defaultdict
from collections import namedtuple

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)

class Planet:
    def __init__(self, position):
        self.position = position
        self.velocity = Vector(0, 0, 0)

    def energy(self):
        return abs(self.position.x) + abs(self.position.y) + abs(self.position.z)

#Vector = namedtuple("Vector", ('x', 'y', 'z'))

def parse_input(input):
    positions = []
    for line in input.strip().split("\n"):
        m = re.match(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>", line)
        positions.append(Vector(int(m.group(1)), int(m.group(2)), int(m.group(3))))
    return positions


def apply_gravity(planets):
    for p1 in planets:
        for p2 in planets:
            if p1 == p2:
                continue
            if p1.position.x > p2.position.x:
                p1.velocity.x -= 1
            elif p1.position.x < p2.position.x:
                p1.velocity.x += 1
            if p1.position.y > p2.position.y:
                p1.velocity.y -= 1
            elif p1.position.y < p2.position.y:
                p1.velocity.y += 1
            if p1.position.z > p2.position.z:
                p1.velocity.z -= 1
            elif p1.position.z < p2.position.z:
                p1.velocity.z += 1


def apply_positions(planets):
    for p in planets:
        p.position = p.position + p.velocity


def solve1(positions, steps):
    step = 0
    planets = [Planet(p) for p in positions]
    for step in range(steps):
        print("Step: {}".format(step))
        for p in planets:
            print("pos: {}, vel: {}".format(p.position, p.velocity))
        apply_gravity(planets)
        apply_positions(planets)


def solve2(positions):
    pass


# Execute tests with:
# python3 -m unittest dayX.py
class TestThis(unittest.TestCase):
    def test1(self):
        pass


if __name__ == "__main__":
    with open("input/day12.txt", "r") as f:
        input = f.read()
    positions = parse_input(input)
    solve1(positions, 10)
