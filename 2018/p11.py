#!/usr/bin/env python3

# By Jakob Ruhe 2018-12-11

import unittest

def calc_power_level(cache, x, y, grid_serial):
    id = "{}_{}".format(x, y)
    if id in cache:
        return cache[id]
    rack_id = x + 10
    power_level = rack_id * y
    power_level += grid_serial
    power_level *= rack_id
    h = (power_level // 100) % 10
    value = h - 5
    cache[id] = value
    return value

def square(cache, cx, cy, grid_serial):
    s = 0
    for y in range(cy - 1, cy + 2):
        for x in range(cx - 1, cx + 2):
            s += calc_power_level(cache, x, y, grid_serial)
    return s

def solve(grid_serial):
    cache = {}
    best_value = None
    best_xy = None
    for cy in range(2, 300):
        for cx in range(2, 300):
            s = square(cache, cx, cy, grid_serial)
            if best_value is None or s > best_value:
                best_value = s
                best_xy = (cx - 1, cy - 1)
    print("Best: {} at {}".format(best_value, best_xy))
    return best_value

class TestThis(unittest.TestCase):
    def test_power_level(self):
        self.assertEqual(calc_power_level({}, 3, 5, 8), 4)
        self.assertEqual(calc_power_level({}, 122, 79, 57), -5)
        self.assertEqual(calc_power_level({}, 217, 196, 39), 0)
        self.assertEqual(calc_power_level({}, 101, 153, 71), 4)
    def test_solve(self):
        self.assertEqual(solve(18), 29)
        self.assertEqual(solve(42), 30)

if __name__ == "__main__":
    #unittest.main()
    solve(7672)
