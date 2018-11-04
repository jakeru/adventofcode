#!/usr/bin/env python3

import unittest
from collections import namedtuple

Tower = namedtuple("Tower", ["name", "weight", "children_names"])

class Tower:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.name_of_children = []
        self.children = []
        self.parent = None
        self.weight_of_children = None
    def __str__(self):
        return "Name: {}, weight: {}, children: {}".format(self.name, self.weight, self.name_of_children)

def remove_chars(str, chars):
    for c in chars:
        str = str.replace(c, '')
    return str

def parse_data(data):
    tower_list = []
    rows = data.strip().split("\n")
    for row in rows:
        parts = remove_chars(row.strip(), "()->,").split()
        tower = Tower(parts[0], int(parts[1]))
        for i in range(2, len(parts)):
            tower.name_of_children.append(parts[i])
        tower_list.append(tower)
    return tower_list

def build_graph(tower_list):
    towers = {}
    for t in tower_list:
        towers[t.name] = t
    for key, t in towers.items():
        for nc in t.name_of_children:
            c = towers[nc]
            assert(c.parent == None)
            c.parent = t
            t.children.append(c)
    return towers

def find_base(towers):
    base = None
    for key, t in towers.items():
        if t.parent is None:
            assert(base is None)
            base = t
    return base

def calc_weight(tower):
    if tower.weight_of_children is not None:
        return tower.weight_of_children + tower.weight
    children_weight = 0
    for t in tower.children:
        children_weight = children_weight + calc_weight(t)
    tower.weight_of_children = children_weight
    return tower.weight_of_children + tower.weight

def is_balanced(tower):
    if len(tower.children) < 2:
        return True
    w1 = calc_weight(tower.children[0])
    for i in range(1, len(tower.children)):
        if calc_weight(tower.children[i]) != w1:
            return False
    return True

def get_unbalanced_without_unbalanced_children(towers):
    result = []
    for key,t in towers.items():
        if is_balanced(t):
            continue
        has_unbalanced_children = False
        for c in t.children:
            if not is_balanced(c):
                has_unbalanced_children = True
                break
        if not has_unbalanced_children:
            result.append(t)
    return result

def divide_in_weight_groups(tower):
    children_weights = {}
    for c in tower.children:
        cw = calc_weight(c)
        if not children_weights.get(cw):
            children_weights[cw] = []
        children_weights[cw].append(c)
    return children_weights

def find_common_towers(groups):
    for k,v in groups.items():
        if len(v) > 1:
            return v
    return None

def find_unique_tower(groups):
    for k,v in g.items():
        if len(v) == 1:
            return v[0]
    return None

class TestThis(unittest.TestCase):
    def test_largest(self):
        data = """
                pbga (66)
                xhth (57)
                ebii (61)
                havc (66)
                ktlj (57)
                fwft (72) -> ktlj, cntj, xhth
                qoyq (66)
                padx (45) -> pbga, havc, qoyq
                tknk (41) -> ugml, padx, fwft
                jptl (61)
                ugml (68) -> gyxo, ebii, jptl
                gyxo (61)
                cntj (57)
                """
        tower_list = parse_data(data)
        towers = build_graph(tower_list)
        base = find_base(towers)
        self.assertEqual(base.name, "tknk")

if __name__ == "__main__":
    #unittest.main()
    with open("input7.txt", "r") as f:
        data = f.read()
        tower_list = parse_data(data)
        print("Number of towers: {}".format(len(tower_list)))
        towers = build_graph(tower_list)
        base = find_base(towers)
        print("Base tower: {}".format(base))

        unbalanced_leafs = get_unbalanced_without_unbalanced_children(towers)
        print("Unbalanced without unbalanced children: {}".format(len(unbalanced_leafs)))
        assert(len(unbalanced_leafs) <= 1)
        for t in unbalanced_leafs:
            print(t)
            print("Weight of {} with children: {}".format(t.name, calc_weight(t)))
            for c in t.children:
                print("  {}".format(c))
                print("  Weight of child {} with its children: {}".format(c.name, calc_weight(c)))
            g = divide_in_weight_groups(t)
            assert(len(g) == 2)
            tu = find_unique_tower(g)
            tc = find_common_towers(g)
            print("  Common weight including their children for {} of the children is: {}".format(len(tc), calc_weight(tc[0])))
            print("  Tower {} has weight including children: {}".format(tu.name, calc_weight(tu)))
            diff = calc_weight(tc[0]) - calc_weight(tu)
            print("  Tower {} should change its weight from {} to {}".format(tu.name, tu.weight, tu.weight + diff))
