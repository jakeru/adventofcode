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


def parse(entries):
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
    return seeds, maps


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
    seeds, maps = parse(entries)

    locations = {}
    for seed in seeds:
        locations[seed] = find_location(seed, maps)

    print(f"locations {locations}")

    return min(locations.values())


Range = namedtuple("Range", ["min", "num"])

# def find_lowest(search_min, search_num, maps):
#     keys = list(reversed(maps.keys()))
#     for m in keys:
#         print(f"map {m}, searching for: {search_min} {search_num}")
#         found = None
#         for e in maps[m]:
#             dest, source, num = e
#             print(f"{dest} {source} {num}")
#             if source >= search_min and source < search_min + search_num:
#                 pass
#
#         search = found if found else search
#     return search


def range_str(r):
    return f"[{r[0]}..{r[0] + r[1] - 1}]" if r[1] > 0 else "[]"


def find_best_location_in_range(r, map_names, maps):
    if not map_names:
        print(f"Returning {r.min}")
        return r.min
    level_maps = sorted(maps[map_names[0]], key=lambda m: m[1])
    best = None
    prev = None
    gaps = []
    for lm in level_maps:
        m = Range(lm[1], lm[2])
        c_min = max(r.min, m.min)
        c_max = min(r.min + r.num - 1, m.min + m.num - 1)
        common = Range(c_min, c_max - c_min + 1)
        if common.num > 0:
            dest = Range(lm[0] + common.min - m.min, common.num)
            print(
                f"At {len(map_names)} {map_names[0]} Evaluating range {range_str(r)} in {range_str(m)}: overlap: {range_str(common)}, dest: {range_str(dest)}"
            )
            best_in_lm = find_best_location_in_range(dest, map_names[1:], maps)
            if best is None or best_in_lm < best:
                best = best_in_lm
            if prev is None and r.min < m.min:
                gaps.append(Range(r.min, m.min - r.min))
                print(
                    f"At {len(map_names)} {map_names[0]} Evaluating range {range_str(r)} in {range_str(m)}: adding gap: {range_str(gaps[-1])}"
                )
            elif prev is not None and prev.min + prev.num < common.min:
                gaps.append(
                    Range(prev.min + prev.num, common.min - (prev.min + prev.num))
                )
                print(
                    f"At {len(map_names)} {map_names[0]} Evaluating range {range_str(r)} in {range_str(m)}: adding gap: {range_str(gaps[-1])}"
                )
            prev = common
    if prev is None:
        gaps.append(r)
        print(
            f"At {len(map_names)} {map_names[0]} Evaluating range {range_str(r)} adding full gap: {range_str(gaps[-1])}"
        )
    elif r.min + r.num > prev.min + prev.num:
        gaps.append(Range(prev.min + prev.num, r.min + r.num - (prev.min + prev.num)))
        print(
            f"At {len(map_names)} {map_names[0]} Evaluating range {range_str(r)} adding last gap: {range_str(gaps[-1])}"
        )

    for g in gaps:
        best_in_gap = find_best_location_in_range(g, map_names[1:], maps)
        if best is None or best_in_gap < best:
            best = best_in_gap

    return best


def find_best_location_in_ranges(ranges, map_names, maps):
    best = None
    for r in ranges:
        best_in_range = find_best_location_in_range(r, map_names, maps)
        if best is None or best_in_range < best:
            best = best_in_range
    return best


def solve2(entries):
    seeds, maps = parse(entries)
    map_names = list(maps.keys())

    ranges = []
    for i in range(0, len(seeds), 2):
        ranges.append(Range(seeds[i], seeds[i + 1]))
    return find_best_location_in_ranges(ranges, map_names, maps)


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
        self.assertEqual(solve2(parse_input(self.input)), 46)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
