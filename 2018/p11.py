#!/usr/bin/env python3

# By Jakob Ruhe 2018-12-11

import unittest

def calc_power_level(x, y, serial):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial
    power_level *= rack_id
    h = (power_level // 100) % 10
    value = h - 5
    return value

def square(minx, miny, size, serial):
    s = 0
    for y in range(miny, miny + size):
        for x in range(minx, minx + size):
            s += calc_power_level(x, y, serial)
    return s

def solve1(serial):
    best_value = None
    best_xy = None
    total_size = 300
    square_size = 3
    for miny in range(1, total_size - square_size + 1):
        for minx in range(1, total_size - square_size + 1):
            s = square(minx, miny, square_size, serial)
            if best_value is None or s > best_value:
                best_value = s
                best_xy = (minx, miny)
    return (best_xy, best_value)

class TestThis(unittest.TestCase):
    def test_power_level(self):
        self.assertEqual(calc_power_level(3, 5, 8), 4)
        self.assertEqual(calc_power_level(122, 79, 57), -5)
        self.assertEqual(calc_power_level(217, 196, 39), 0)
        self.assertEqual(calc_power_level(101, 153, 71), 4)
    def test_solve1(self):
        self.assertEqual(solve1(18), ((33, 45), 29))
        self.assertEqual(solve1(42), ((21, 61), 30))

if __name__ == "__main__":
    #unittest.main()
    (p1, b1) = solve1(7672)
    print("The answer to subproblem 1 is: {} ({})".format(",".join(map(lambda e: str(e), p1)), b1))
    print("Use the solution written in C to solve subproblem 2.")
