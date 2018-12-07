#!/usr/bin/env python3

# By Jakob Ruhe 2018-12-06

import unittest
import collections
import re

Coord = collections.namedtuple('Coord', ['x', 'y'])

def dist(c1, c2):
    return abs(c2.x-c1.x) + abs(c2.y-c1.y)

def min_max(coords):
    min_x = coords[0].x
    min_y = coords[0].y
    max_x = coords[0].x
    max_y = coords[0].y
    for c in coords:
        if c.x < min_x:
            min_x = c.x
        if c.y < min_y:
            min_y = c.y
        if c.x > max_x:
            max_x = c.x
        if c.y > max_y:
            max_y = c.y
    return (Coord(min_x, min_y), Coord(max_x, max_y))

def closest_coords(coords, coord):
    closest = []
    closest_dist = None
    for i in range(len(coords)):
        d = dist(coords[i], coord)
        if closest_dist is None or d < closest_dist:
            closest = [i]
            closest_dist = d
        elif d == closest_dist:
            closest.append(i)
    return closest

def find_largest_area(coords):
    print("Number of coords: {}".format(len(coords)))
    (min_c, max_c) = min_max(coords)
    width = max_c.x - min_c.x
    height = max_c.y - min_c.y
    print("Coords min: {}, max: {}".format(min_c, max_c))
    print("Locations: {} x {} = {}".format(width, height, width * height))
    areas = {}
    infinite_areas = {}
    for y in range(min_c.y, max_c.y + 1):
        for x in range(min_c.x, max_c.x + 1):
            closest = closest_coords(coords, Coord(x, y))
            if len(closest) > 1:
                continue
            assert(len(closest) == 1)
            if y == min_c.y or y == max_c.y or x == min_c.x or x == max_c.x:
                for i in closest:
                    infinite_areas[i] = True
                continue
            i = closest[0]
            if not i in areas:
                areas[i] = 1
            else:
                areas[i] += 1
    for key in infinite_areas:
        if key in areas:
            del areas[key]
    largest_area = max(areas.keys(), key=(lambda key: areas[key]))
    print("Largest area has index {} and an area of: {}".format(largest_area, areas[largest_area]))
    return areas[largest_area]

def is_within_distance(coords, max_dist, p):
    dist_sum = 0
    for d in coords:
        dist_sum += dist(d, p)
        if dist_sum >= max_dist:
            return False
    return True

def find_size_of_region_within(coords, max_dist):
    print("Number of coords: {}".format(len(coords)))
    margin = max_dist // len(coords)
    print("Margin: {}".format(margin))
    (min_c, max_c) = min_max(coords)
    left = min_c.x - margin
    right = max_c.x + margin
    top = min_c.y - margin
    bottom = max_c.y + margin
    width = right - left
    height = bottom - top
    print("Coords min: {}, max: {}".format(min_c, max_c))
    print("Locations: {} x {} = {}".format(width, height, width * height))
    size_within = 0
    for y in range(top, bottom + 1):
        for x in range(left, right + 1):
            if is_within_distance(coords, max_dist, Coord(x, y)):
                assert(y != top and y != bottom and x != left and x != right)
                size_within += 1
    return size_within

class TestThis(unittest.TestCase):
    coords = [
        Coord(1, 1),
        Coord(1, 6),
        Coord(8, 3),
        Coord(3, 4),
        Coord(5, 5),
        Coord(8, 9),
    ]
    def test_dist(self):
        self.assertEqual(dist(Coord(10, 20), Coord(11, 2)), 1+18)
        self.assertEqual(dist(Coord(10, 20), Coord(10, 20)), 0)
    def test_find_largest_area(self):
        self.assertEqual(find_largest_area(self.coords), 17)
    def test_find_size_of_region_within(self):
        self.assertEqual(find_size_of_region_within(self.coords, 32), 16)

if __name__ == "__main__":
    #unittest.main()
    coords = []
    with open("p6_input.txt", "r") as f:
        lines = f.readlines()
    for line in lines:
        m = re.match(r"(\d+), (\d+)", line)
        coords.append(Coord(int(m.group(1)), int(m.group(2))))
    largest_area = find_largest_area(coords)
    print("The answer to subproblem 1 is: {}".format(largest_area))
    size_within = find_size_of_region_within(coords, 10000)
    print("The answer to subproblem 2 is: {}".format(size_within))
