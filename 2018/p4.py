#!/usr/bin/env python3

# By Jakob Ruhe 2018-12-04

import unittest
import collections
import re
import datetime
from enum import Enum

class EventType:
    shift_begin = 1
    falls_asleep = 2
    wakes_up = 3

def get_input(file):
    with open(file, "r") as f:
        return f.readlines()

def date_from_str(str):
    m = re.search(r"\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\]", str)
    params = [int(m.group(i)) for i in range(1,6)]
    return datetime.datetime(*params)

def type_and_guard_from_str(str):
    m = re.search(r"\] Guard #(\d+) begins shift", str)
    if m is not None:
        return (EventType.shift_begin, int(m.group(1)))
    m = re.search(r"\] falls asleep", str)
    if m is not None:
        return (EventType.falls_asleep, None)
    m = re.search(r"\] wakes up", str)
    if m is not None:
        return (EventType.wakes_up, None)
    raise ValueError("Unknown event type: {}".format(str))

def update_histogram(histogram, start, end):
    for i in range(start, end):
        if not i in histogram:
            histogram[i] = 0
        histogram[i] = histogram[i] + 1

class Event:
    def __init__(self, line):
        self.time = date_from_str(line)
        (self.type, self.guard) = type_and_guard_from_str(line)
    def sort_key(self):
        return self.time
    def __str__(self):
        return str(self.time) + ": " + str(self.type) + " " + str(self.guard)

class Guard:
    def __init__(self, id):
        self.id = id
        self.time_slept = 0
        self.sleep_histogram = {}
    def add_sleep(self, start, end):
        time_slept_now = int((end - start).total_seconds() / 60)
        self.time_slept += time_slept_now
        if time_slept_now >= 60:
            raise ValueError("{} must not sleep more than 60 minutes: {}, start: {} end: {}".format(self, time_slept_now, start, end))
        if start.hour != 0 or end.hour != 0:
            raise ValueError("{} should only sleep between 00 and 01, not start: {} end: {}".format(self, start, end))
        update_histogram(self.sleep_histogram, start.minute, end.minute)
    def get_minute_usually_asleep(self):
        return max(self.sleep_histogram.keys(), key=(lambda key: self.sleep_histogram[key]))
    def __str__(self):
        return "#{}: {} minutes".format(self.id, self.time_slept)

def sleep_calc(events):
    guards = {}
    guard = None
    sleeping_since = None
    for e in events:
        if e.type == EventType.shift_begin:
            if sleeping_since is not None:
                raise ValueError("Guard {} is still asleep: {}".format(guard, e))
            guard = e.guard
        elif e.type == EventType.falls_asleep:
            if guard is None:
                raise ValueError("No guard onduty: {}".format(e))
            if sleeping_since is not None:
                raise ValueError("Guard is already sleeping: {}".format(e))
            sleeping_since = e.time
        elif e.type == EventType.wakes_up:
            if sleeping_since is None:
                raise ValueError("Guard {} is not sleeping: {}".format(guard, e))
            if not guard in guards:
                guards[guard] = Guard(guard)
            guards[guard].add_sleep(sleeping_since, e.time)
            sleeping_since = None
    return guards

def get_id_of_guard_that_slept_most(guards):
    return max(guards.keys(), key=(lambda key: guards[key].time_slept))

def read_and_sort(file):
    lines = get_input(file)
    events = []
    for line in lines:
        events.append(Event(line))
    events.sort(key=Event.sort_key)
    return events

def solve1(guards):
    id = get_id_of_guard_that_slept_most(guards)
    usually_sleeps = guards[id].get_minute_usually_asleep()
    result = id * usually_sleeps
    print("Guard {} is usually asleep at minute {}: {} times".format(
        guards[id], usually_sleeps, guards[id].sleep_histogram[usually_sleeps]))
    print("The answer for problem 1 is: {}".format(result))
    return result

def get_id_of_guard_that_sleeps_most_at_a_specific_time(guards):
    return max(guards.keys(), key=(lambda key: guards[key].sleep_histogram[guards[key].get_minute_usually_asleep()]))

def solve2(guards):
    id = get_id_of_guard_that_sleeps_most_at_a_specific_time(guards)
    usually_sleeps = guards[id].get_minute_usually_asleep()
    result = id * usually_sleeps
    print("Guard {} is usually asleep at minute {}: {} times".format(
        guards[id], usually_sleeps, guards[id].sleep_histogram[usually_sleeps]))
    print("The answer for problem 2 is: {}".format(result))
    return result

class TestThis(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(date_from_str("[1518-11-01 02:03] Guard #10 begins shift"), datetime.datetime(1518, 11, 1, 2, 3))
        self.assertEqual(type_and_guard_from_str("[1518-11-01 02:03] Guard #10 begins shift"), (EventType.shift_begin, 10))
        self.assertEqual(type_and_guard_from_str("[1518-11-01 00:05] falls asleep"), (EventType.falls_asleep, None))
        self.assertEqual(type_and_guard_from_str("[1518-11-01 00:25] wakes up"), (EventType.wakes_up, None))
    def test_solve(self):
        events = read_and_sort("p4_test_input.txt")
        guards = sleep_calc(events)
        self.assertEqual(solve1(guards), 240)
        self.assertEqual(solve2(guards), 4455)

if __name__ == "__main__":
    #unittest.main()
    events = read_and_sort("p4_input.txt")
    guards = sleep_calc(events)
    solve1(guards)
    solve2(guards)
