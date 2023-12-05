#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-05

import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple
import utils


def parse_input(input):
    return input.strip().split("\n")


def find_location(seed, maps):
    keys = list(maps.keys())
    search = seed
    for m in keys:
        print(f"map {m}, searching for: {search}")
        found = None
        for e in maps[m]:
            dest, source, num = e
            print(f"{dest} {source} {num}")
            if search >= source and search < source + num:
                found = dest + search - source
                break
        search = found if found else search
    return search


def solve1(entries):
    sections = "\n".join(entries).split("\n\n")
    print(sections)
    seeds = []
    map_name = None
    maps = defaultdict(list)
    for section in sections:
        line = section.split("\n")[0]
        if line.startswith("seeds:"):
            seeds = [int(w) for w in line.split(":")[1].strip().split()]
            print(f"seeds {seeds}")
            continue
        else:
            map_name = line.split(" ")[0]
        for line in section.split("\n")[1:]:
            numbers = [int(w) for w in line.split()]
            print(f"{map_name}: {numbers}")
            maps[map_name].append(numbers)

    print(f"maps: {list(maps.keys())}")

    locations = {}
    for seed in seeds:
        locations[seed] = find_location(seed, maps)


    print(f"locations {locations}")

    return min(locations.values())


def solve2(entries):
    pass


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 35)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), None)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
