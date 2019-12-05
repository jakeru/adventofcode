#!/usr/bin/env python3

# By Jakob Ruhe 2019-12-05
# Started at 06:21
# P1 solved at 06:57

import unittest

def parse_input(input: str):
    return list(map(int, input.split(",")))


def fetch_parameters(memory, pc, modes, num):
    params = []
    for i in range(0, num):
        m = modes % 10
        modes = modes // 10
        if m == 0:
            params.append(memory[memory[pc + 1 + i]])
        elif m == 1:
            params.append(memory[pc + 1 + i])
        else:
            raise ValueError("Bad param mode: {} pc: {}".format(m, pc))
    return params


def execute(program):
    output = 0
    input = 1
    memory = program.copy()
    pc = 0
    while True:
        op_code = memory[pc] % 100
        if op_code == 1:
            params = fetch_parameters(memory, pc, memory[pc] // 100, 2)
            memory[memory[pc+3]] = params[0] + params[1]
            pc += 4
        elif op_code == 2:
            params = fetch_parameters(memory, pc, memory[pc] // 100, 2)
            memory[memory[pc+3]] = params[0] * params[1]
            pc += 4
        elif op_code == 3:
            memory[memory[pc + 1]] = input
            pc += 2
        elif op_code == 4:
            params = fetch_parameters(memory, pc, memory[pc] // 100, 1)
            output = params[0]
            pc += 2
        elif op_code == 99:
            return output
        else:
            raise ValueError("Unknown op_code: {} at {}".format(op_code, pc))


def solve1():
    with open("input/day5.txt", "r") as f:
        input = f.read()
    program = parse_input(input)
    result = execute(program)
    print("{}".format(result))


def solve2():
    with open("input/day2.txt", "r") as f:
        input = f.read()
    program = parse_input(input)
    for noun in range(0, 100):
        for verb in range(0, 100):
            program[1] = noun
            program[2] = verb
            memory = execute(program)
            if memory[0] == 19690720:
                print("Noun: {}, verb: {}, result: {}".format(noun, verb, noun * 100 + verb))
                return


class TestThis(unittest.TestCase):
    def test1(self):
        self.assertEqual(execute(parse_input("1002,4,3,4,33")), [1002,4,3,4,99])


if __name__ == "__main__":
    solve1()

