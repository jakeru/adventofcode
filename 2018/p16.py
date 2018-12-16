#!/usr/bin/env python3

# By Jakob Ruhe 2018-12-16

import unittest
import re
import io

op_codes = {
    "addr": lambda instr, regs: regs[instr[1]] + regs[instr[2]],
    "addi": lambda instr, regs: regs[instr[1]] + instr[2],
    "mulr": lambda instr, regs: regs[instr[1]] * regs[instr[2]],
    "muli": lambda instr, regs: regs[instr[1]] * instr[2],
    "banr": lambda instr, regs: regs[instr[1]] & regs[instr[2]],
    "bani": lambda instr, regs: regs[instr[1]] & instr[2],
    "borr": lambda instr, regs: regs[instr[1]] | regs[instr[2]],
    "bori": lambda instr, regs: regs[instr[1]] | instr[2],
    "setr": lambda instr, regs: regs[instr[1]],
    "seti": lambda instr, regs: instr[1],
    "gtir": lambda instr, regs: 1 if instr[1] > regs[instr[2]] else 0,
    "gtri": lambda instr, regs: 1 if regs[instr[1]] > instr[2] else 0,
    "gtrr": lambda instr, regs: 1 if regs[instr[1]] > regs[instr[2]] else 0,
    "eqir": lambda instr, regs: 1 if instr[1] == regs[instr[2]] else 0,
    "eqri": lambda instr, regs: 1 if regs[instr[1]] == instr[2] else 0,
    "eqrr": lambda instr, regs: 1 if regs[instr[1]] == regs[instr[2]] else 0,
}

class Sample:
    def __init__(self, before, instr, after):
        self.before = before
        self.instr = instr
        self.after = after
    def __str__(self):
        return str({"before": self.before, "instr": self.instr, "after": self.after})

def parse_instr(stream):
    line = stream.readline()
    m = re.match(r"(\d+) (\d+) (\d+) (\d+)", line)
    if m is None:
        return None
    return list(map(lambda i: int(m.group(i)), range(1, 5)))

def parse_sample(stream):
    line = stream.readline()
    m = re.match(r"Before: \[(\d+), (\d+), (\d+), (\d+)\]", line)
    if m is None:
        return None
    before = list(map(lambda i: int(m.group(i)), range(1, 5)))
    instr = parse_instr(stream)
    assert(instr is not None)
    line = stream.readline()
    m = re.match(r"After:\s+\[(\d+), (\d+), (\d+), (\d+)\]", line)
    after = list(map(lambda i: int(m.group(i)), range(1, 5)))
    line = stream.readline()
    return Sample(before, instr, after)

def get_possible_op_codes(sample):
    possible = []
    for name,exec in op_codes.items():
        result = sample.before.copy()
        result[sample.instr[3]] = exec(sample.instr, sample.before)
        if result == sample.after:
            possible.append(name)
    return possible

def solve1(samples):
    num_three_or_more = 0
    for sample in samples:
        possible = get_possible_op_codes(sample)
        if len(possible) >= 3:
            num_three_or_more += 1
    return num_three_or_more

def find_out_op_codes(samples, instructions):
    ops_not_possible = {}
    for sample in samples:
        possible = get_possible_op_codes(sample)
        op_num = sample.instr[0]
        if not op_num in ops_not_possible:
            ops_not_possible[op_num] = {}
        for op in op_codes:
            if not op in possible:
                ops_not_possible[op_num][op] = True
    ops_possible = {}
    for op_num in sorted(ops_not_possible.keys()):
        possible = []
        for opp in op_codes:
            if not opp in ops_not_possible[op_num]:
                possible.append(opp)
        ops_possible[op_num] = possible
        print("op: {}, possible: {}".format(op_num, ",".join(possible)))
    ops_completed = {}
    while len(ops_possible) > 0:
        found_one = None
        for op_num in ops_possible:
            if len(ops_possible[op_num]) == 1:
                found_one = op_num
        if found_one is None:
            print("Cannot solve this =(")
            print(ops_possible)
            print(ops_completed)
            return None
        op = ops_possible[found_one][0]
        ops_completed[found_one] = op
        del ops_possible[found_one]
        for op_num in ops_possible:
            if op in ops_possible[op_num]:
                ops_possible[op_num].remove(op)
    for op_num in sorted(ops_completed.keys()):
        print("{}: {}".format(op_num, ops_completed[op_num]))
    return ops_completed

def solve2(samples, instructions):
    op_names = find_out_op_codes(samples, instructions)
    assert(op_codes is not None)
    regs = [0, 0, 0, 0]
    for instr in instructions:
        op_name = op_names[instr[0]]
        exec = op_codes[op_name]
        regs[instr[3]] = exec(instr, regs)
    return regs

class TestThis(unittest.TestCase):
    def test_parse_sample(self):
        str = "Before: [3, 2, 1, 1]\n9 2 1 2\nAfter:  [3, 2, 2, 1]\n"
        stream = io.StringIO(str)
        sample = parse_sample(stream)
        self.assertEqual(sample.before, [3, 2, 1, 1])
        self.assertEqual(sample.instr, [9, 2, 1, 2])
        self.assertEqual(sample.after, [3, 2, 2, 1])
    def test_possible(self):
        str = "Before: [3, 2, 1, 1]\n9 2 1 2\nAfter:  [3, 2, 2, 1]\n"
        sample = parse_sample(io.StringIO(str))
        possible = get_possible_op_codes(sample)
        self.assertEqual(sorted(possible), ["addi", "mulr", "seti"])
    def test_solve(self):
        str = "Before: [3, 2, 1, 1]\n9 2 1 2\nAfter:  [3, 2, 2, 1]\n"
        sample = parse_sample(io.StringIO(str))
        samples = [sample]
        self.assertEqual(solve1(samples), 1)

if __name__ == "__main__":
    #unittest.main()
    samples = []
    instructions = []
    with open("p16_input.txt") as f:
        while True:
            sample = parse_sample(f)
            if sample is None:
                break
            samples.append(sample)
        f.readline()
        while True:
            instr = parse_instr(f)
            if not instr:
                break
            instructions.append(instr)
    print("Number of samples: {}".format(len(samples)))
    num_three_or_more = solve1(samples)
    print("P1: Number of samples behaving like three or more opcodes: {}".format(num_three_or_more))
    print("Number of instructions: {}".format(len(instructions)))
    regs = solve2(samples, instructions)
    print("P2: Register 0 after execution: {}".format(regs[0]))
