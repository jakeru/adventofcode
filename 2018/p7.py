#!/usr/bin/env python3

# By Jakob Ruhe 2018-12-07

import unittest
import collections
import re

Req = collections.namedtuple('Req', ['before', 'after'])

class Step:
    def __init__(self, name):
        self.name = name
        self.steps_to_finish_before = {}
    def __str__(self):
        return self.name

def req_from_str(str):
    m = re.match(r"Step ([A-Z]) must be finished before step ([A-Z]) can begin.", str)
    return Req(m.group(1), m.group(2))

def get_reqs(file):
    reqs = []
    with open(file, "r") as f:
        for line in f.readlines():
            req = req_from_str(line)
            assert(req.after != req.before)
            reqs.append(req)
    return reqs

def get_steps(reqs):
    steps = {}
    for r in reqs:
        steps[r.before] = True
        steps[r.after] = True
    return sorted(steps.keys())

def build_step_dict(steps):
    step_dict = {}
    for s in steps:
        step_dict[s] = Step(s)
    return step_dict

def apply_reqs(step_dict, reqs):
    for s in step_dict:
        for r in reqs:
            if r.after == s:
                step_dict[s].steps_to_finish_before[r.before] = step_dict[r.before]

def is_next_step(step_dict, step):
    for before in step.steps_to_finish_before.values():
        if before.name in step_dict:
            return False
    return True

def find_next_step(step_dict):
    for key in sorted(step_dict.keys()):
        if is_next_step(step_dict, step_dict[key]):
            return step_dict[key]
    raise ValueError("No available step")

def find_next_step_not_ongoing(step_dict, ongoing_dict):
    for key in sorted(step_dict.keys()):
        if key in ongoing_dict:
            continue
        if is_next_step(step_dict, step_dict[key]):
            return step_dict[key]
    return None

def walk_step_list(step_dict):
    walk_list = []
    while step_dict:
        step = find_next_step(step_dict)
        del step_dict[step.name]
        walk_list.append(step.name)
    return walk_list

def solve1(file):
    reqs = get_reqs(file)
    steps = get_steps(reqs)
    step_dict = build_step_dict(steps)
    apply_reqs(step_dict, reqs)
    return walk_step_list(step_dict)

class Worker:
    def __init__(self, name):
        self.name = name
        self.step = None
        self.time_left = 0
    def __str__(self):
        return self.name
    def start_work(self, now, step, time_to_finish):
        assert(self.step is None)
        self.step = step
        self.time_left = time_to_finish
        print("At {} worker {} starts on step {}. It will take {} s".format(now, self.name, step, time_to_finish))
    def forward_time(self, now, elapsed_time):
        if self.step is None:
            return None
        self.time_left -= elapsed_time
        assert(self.time_left >= 0)
        if self.time_left == 0:
            print("At {} worker {} finished step {}".format(now, self.name, self.step))
            finished_step = self.step
            self.step = None
            return finished_step
        return None

def time_to_wait_for_a_worker(workers):
    w = min(workers, key=lambda w: w.time_left)
    return w.time_left

def forward_time(now, workers, elapsed_time, step_dict, ongoing_dict, walk_list):
    for w in workers:
        finished_step = w.forward_time(now, elapsed_time)
        if finished_step is not None:
            del ongoing_dict[finished_step.name]
            del step_dict[finished_step.name]
            walk_list.append(finished_step.name)

def get_first_free_worker(workers):
    for w in workers:
        if w.step is None:
            return w
    return None

def get_first_free_worker_working(workers):
    first = None
    for w in workers:
        if w.step is not None and (first is None or w.time_left < first.time_left):
            first = w
    return first

def timed_walk(step_dict, workers, time_function):
    time = 0
    walk_list = []
    ongoing_dict = {}
    while step_dict:
        elapsed_time = time_to_wait_for_a_worker(workers)
        time += elapsed_time
        forward_time(time, workers, elapsed_time, step_dict, ongoing_dict, walk_list)
        worker = get_first_free_worker(workers)
        assert(worker is not None)
        step = find_next_step_not_ongoing(step_dict, ongoing_dict)
        if step is None:
            w = get_first_free_worker_working(workers)
            assert(w is not None)
            elapsed_time = w.time_left
            print("At {} forwarding time {} s for worker {} to finish step {}".format(time, elapsed_time, w, w.step))
            time += elapsed_time
            forward_time(time, workers, elapsed_time, step_dict, ongoing_dict, walk_list)
            assert(get_first_free_worker(workers) is not None)
        else:
            worker.start_work(time, step, time_function(step.name))
            ongoing_dict[step.name] = step
    return (walk_list, time)

def solve2(file, num_workers, time_function):
    reqs = get_reqs(file)
    steps = get_steps(reqs)
    step_dict = build_step_dict(steps)
    apply_reqs(step_dict, reqs)
    workers = []
    for i in range(num_workers):
        workers.append(Worker(str(i + 1)))
    return timed_walk(step_dict, workers, time_function)

class TestThis(unittest.TestCase):
    def test_get_req_from_str(self):
        self.assertEqual(req_from_str("Step A must be finished before step D can begin."), Req("A", "D"))
    def test_get_steps(self):
        reqs = get_reqs("p7_test_input.txt")
        self.assertEqual(len(reqs), 7)
        steps = get_steps(reqs)
        self.assertEqual(steps, ["A", "B", "C", "D", "E", "F"])
    def test_solve1(self):
        self.assertEqual(solve1("p7_test_input.txt"), ["C", "A", "B", "D", "F", "E"])
    def test_solve2(self):
        time_function = lambda step: 1 + ord(step) - ord("A")
        self.assertEqual(solve2("p7_test_input.txt", 2, time_function), (["C", "A", "B", "F", "D", "E"], 15))

if __name__ == "__main__":
    #unittest.main()
    result1 = solve1("p7_input.txt")
    print("The result for subproblem 1 is: {}".format("".join(result1)))
    time_function = lambda step: 61 + ord(step) - ord("A")
    (walk_list, time) = solve2("p7_input.txt", 5, time_function)
    print("Walk list: {}".format("".join(walk_list)))
    print("The result for subproblem 2 is: {}".format(time))
