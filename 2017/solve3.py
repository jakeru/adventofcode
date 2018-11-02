#!/usr/bin/env python3

# Spiral pattern:
# 17  16  15  14  13
# 18   5   4   3  12
# 19   6   1   2  11
# 20   7   8   9  10
# 21  22  23---> ...

# How many steps to go from square N to 1 using Manhattan Distance?
#  1: 0
#  2: 1
#  3: 2
#  4: 1
#  5: 2
#  6: 1
#  7: 2
#  8: 1
#  9: 2
# 10: 3
# 11: 2
# 12: 3
# 13: 4

# From square 361527 to 1?

# The Manhattan distance is:
# Number of steps x + number of steps y
# Let 1 be at position (0,0)
# How to calculate the position of N?
# Brute force?
# How many digits in each ring?
# 0: 1
# 1: 3+3+1+1 6+2    8
# 2: 5+5+3+3 10+6   16
# 3: 7+7+5+5 14+10  24
# 4: 9+9+7+7 18+14  32
# 5: 11+11+9+9 22+18 40
# 6: 13+13+11+11 26+22 48

# Rewrite a bit
# 1: (1+3) * 2
# 2: (3+5) * 2
# 3: (5+7) * 2
# 4: (7+9) * 2
# 5: (9+11) * 2
# R(n): () * 2

# Digits in ring
# 0: 1
# 1: 2...9
# 2: 10...25
# 3: 26...49

# OK, so it is quite straight forward to see in which ring we are:

import unittest
from collections import namedtuple

cache = {}

def cache_get(type, key):
    c = cache.get(type)
    if c is None:
        return None
    return c.get(key)

def cache_set(type, key, value):
    if not type in cache:
        cache[type] = {}
    cache[type][key] = value
    return value

def digits_in_ring(r):
    if r == 0:
        return 1
    return 8 * r

def first_in_ring(r):
    c = cache_get('first_in_ring', r)
    if c is not None:
        return c
    sum = 1
    for i in range(0, r):
        sum += digits_in_ring(i)
    return cache_set('first_in_ring', r, sum)

def last_in_ring(r):
    return first_in_ring(r) + digits_in_ring(r) - 1

def ring(n):
    c = cache_get('ring', n)
    if c is not None:
        return c
    r = 0
    first = first_in_ring(r)
    while True:
        next = first + digits_in_ring(r)
        if n >= first and n < next:
            return cache_set('ring', n, r)
        first = next
        r = r + 1

def corners(r):
    Corners = namedtuple('Corners', ['top_right', 'top_left', 'bottom_left', 'bottom_right'])
    if r == 0:
        return Corners(1, 1, 1, 1)
    d = r * 2 + 1
    first = first_in_ring(r)
    top_right = first - 1 + d - 1
    top_left = top_right + d - 1
    bottom_left = top_left + d - 1
    bottom_right = bottom_left + d - 1
    return Corners(top_right, top_left, bottom_left, bottom_right)

def position_x(n, r, c):
    if n <= c.top_right:
        # right
        return r
    elif n <= c.top_left:
        # top
        return -r + c.top_left - n
    elif n <= c.bottom_left:
        # left
        return -r
    else:
        # bottom
        return -r + n - c.bottom_left

def position_y(n, r, c):
    if n <= c.top_right:
        # right
        return r + n - c.top_right
    elif n <= c.top_left:
        # top
        return r
    elif n <= c.bottom_left:
        # left
        return -r + c.bottom_left - n
    else:
        # bottom
        return -r

def position(n):
    c = cache_get('position', n)
    if c is not None:
        return c
    r = ring(n)
    c = corners(r)
    x = position_x(n, r, c)
    y = position_y(n, r, c)
    Point = namedtuple('Point', ['x', 'y'])
    return cache_set('position', n, Point(x, y))

def is_neighbors(p1, p2):
    return abs(p1[0] - p2[0]) <= 1 and abs(p1[1] - p2[1]) <= 1

def sum_at(n):
    c = cache_get('sum_at', n)
    if c is not None:
        return c
    if n == 1:
        return 1
    pn = position(n)
    sum = 0;
    for i in range(1, n):
        pi = position(i)
        if is_neighbors(pn, pi):
            sum += sum_at(i)
    return cache_set('sum_at', n, sum)

def first_larger_than(ref):
    n = 1
    while True:
        sum = sum_at(n)
        if sum > ref:
            return (n, sum)
        n = n + 1

class TestSum(unittest.TestCase):
    def test_cache(self):
        self.assertEqual(cache_get('test', 23), None)
        cache_set('test', 23, 42)
        self.assertEqual(cache_get('test', 23), 42)

    def test_digits_in_ring(self):
        self.assertEqual(digits_in_ring(0), 1)
        self.assertEqual(digits_in_ring(1), 8)
        self.assertEqual(digits_in_ring(2), 16)
        self.assertEqual(digits_in_ring(3), 24)
        self.assertEqual(digits_in_ring(4), 32)

    def test_first_in_ring(self):
        self.assertEqual(first_in_ring(0), 1)
        self.assertEqual(first_in_ring(1), 2)
        self.assertEqual(first_in_ring(2), 10)
        self.assertEqual(first_in_ring(3), 26)
        self.assertEqual(first_in_ring(4), 50)

    def test_ring(self):
        self.assertEqual(ring(1), 0)
        self.assertEqual(ring(2), 1)
        self.assertEqual(ring(9), 1)
        self.assertEqual(ring(10), 2)
        self.assertEqual(ring(25), 2)
        self.assertEqual(ring(26), 3)
        self.assertEqual(ring(49), 3)
        self.assertEqual(ring(50), 4)

    def test_corners(self):
        self.assertEqual(corners(0), (1, 1, 1, 1))
        self.assertEqual(corners(1), (3, 5, 7, 9))
        self.assertEqual(corners(2), (13, 17, 21, 25))

    def test_position(self):
        self.assertEqual(position(1), (0, 0))
        self.assertEqual(position(2), (1, 0))
        self.assertEqual(position(3), (1, 1))
        self.assertEqual(position(4), (0, 1))
        self.assertEqual(position(5), (-1, 1))
        self.assertEqual(position(6), (-1, 0))
        self.assertEqual(position(7), (-1, -1))
        self.assertEqual(position(8), (0, -1))
        self.assertEqual(position(9), (1, -1))
        self.assertEqual(position(10), (2, -1))
        self.assertEqual(position(11), (2, 0))
        self.assertEqual(position(12), (2, 1))
        self.assertEqual(position(13), (2, 2))
        self.assertEqual(position(14), (1, 2))
        self.assertEqual(position(15), (0, 2))
        self.assertEqual(position(16), (-1, 2))
        self.assertEqual(position(17), (-2, 2))
        self.assertEqual(position(18), (-2, 1))
        self.assertEqual(position(19), (-2, 0))
        self.assertEqual(position(20), (-2, -1))
        self.assertEqual(position(21), (-2, -2))
        self.assertEqual(position(22), (-1, -2))
        self.assertEqual(position(23), (0, -2))
        self.assertEqual(position(24), (1, -2))
        self.assertEqual(position(25), (2, -2))
        self.assertEqual(position(26), (3, -2))
        self.assertEqual(position(27), (3, -1))

    def test_is_neighbors(self):
        self.assertTrue(is_neighbors((20, 40), (21, 40)))
        self.assertTrue(is_neighbors((20, 40), (21, 41)))
        self.assertTrue(is_neighbors((20, 40), (20, 41)))
        self.assertTrue(is_neighbors((20, 40), (19, 41)))
        self.assertTrue(is_neighbors((20, 40), (19, 40)))
        self.assertTrue(is_neighbors((20, 40), (19, 39)))
        self.assertTrue(is_neighbors((20, 40), (20, 39)))
        self.assertTrue(is_neighbors((20, 40), (21, 39)))
        self.assertFalse(is_neighbors((20, 40), (22, 40)))

    def test_sum_at(self):
        self.assertEqual(sum_at(1), 1)
        self.assertEqual(sum_at(2), 1)
        self.assertEqual(sum_at(3), 2)
        self.assertEqual(sum_at(4), 4)
        self.assertEqual(sum_at(5), 5)
        self.assertEqual(sum_at(6), 10)
        self.assertEqual(sum_at(7), 11)
        self.assertEqual(sum_at(8), 23)
        self.assertEqual(sum_at(9), 25)
        self.assertEqual(sum_at(10), 26)
        self.assertEqual(sum_at(11), 54)
        self.assertEqual(sum_at(12), 57)
        self.assertEqual(sum_at(13), 59)
        self.assertEqual(sum_at(14), 122)
        self.assertEqual(sum_at(15), 133)
        self.assertEqual(sum_at(16), 142)
        self.assertEqual(sum_at(17), 147)
        self.assertEqual(sum_at(18), 304)
        self.assertEqual(sum_at(19), 330)
        self.assertEqual(sum_at(20), 351)
        self.assertEqual(sum_at(21), 362)
        self.assertEqual(sum_at(22), 747)
        self.assertEqual(sum_at(23), 806)

    def test_first_larger_than(self):
        self.assertEqual(first_larger_than(1), (3, 2))
        self.assertEqual(first_larger_than(2), (4, 4))
        self.assertEqual(first_larger_than(4), (5, 5))
        self.assertEqual(first_larger_than(26), (11, 54))
        self.assertEqual(first_larger_than(805), (23, 806))

if __name__ == "__main__":
    #unittest.main()
    n = 361527
    r = ring(n)
    print("ring({}): {}".format(n, r))
    p = position(n)
    print("position({}): {}".format(n, p))
    d = abs(p.x) + abs(p.y)
    print("Manhattan distance for n={}: {}".format(n, d))
    (ln, lsum) = first_larger_than(n)
    print("At position {} the value {} is written which is larger than {}".format(ln, lsum, n))
