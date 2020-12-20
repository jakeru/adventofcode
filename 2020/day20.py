#!/usr/bin/env python3

# By Jakob Ruhe 2020-12-20
# 07:18: started
# 08:08: p1 solved

import os
import re
import unittest
from collections import defaultdict
from collections import namedtuple

def parse_input(input):
    lines = input.strip().split("\n")
    tiles = {}
    i = 0
    num_tile_lines = 10
    while i < len(lines):
        print(i, lines[i])
        m = re.match(r"Tile (\d+):", lines[i])
        tile_id = int(m.group(1))
        tile_lines = lines[i+1:i+num_tile_lines+1]
        tiles[tile_id] = tile_lines
        i += num_tile_lines + 2
    return tiles

def get_edge(tile, edge):
    if edge == 0:
        return tile[0]
    elif edge == 1:
        return "".join([line[0] for line in tile])
    elif edge == 2:
        return tile[-1]
    elif edge == 3:
        return "".join([line[-1] for line in tile])
    else:
        raise ValueError("edge", edge)

def solve1(tiles):
    for i, t in tiles.items():
        print("Tile", i, t)
    edge_hashes = defaultdict(list)
    for i, tile in tiles.items():
        for e in range(4):
            edge = get_edge(tile, e)
            edge_hashes[hash(edge)].append(i)
            edge_hashes[hash(edge[::-1])].append(i)
    for h,ids in edge_hashes.items():
        print("edge_hash", h, ids)
    tile_unique_edge_count = defaultdict(int)
    for h,ids in edge_hashes.items():
        if len(ids) == 1:
            tile_unique_edge_count[ids[0]] += 1
    corner_tids = []
    for tid, count in tile_unique_edge_count.items():
        print("tile_unique", tid, count)
        if count == 4:
            corner_tids.append(tid)
    for tid in corner_tids:
        print("corner", tid)
    res = 1
    for tid in corner_tids:
        res *= tid
    return res

def solve2(entries):
    pass

# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
"""
    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 20899048083289)
    def test2(self):
        #self.assertEqual(solve2(parse_input(self.input)), None)
        pass

if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
