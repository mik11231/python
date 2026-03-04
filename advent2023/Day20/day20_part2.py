#!/usr/bin/env python3
"""Advent of Code 2023 Day 20 Part 2 - Pulse Propagation.

Find the minimum button presses for module 'rx' to receive a low pulse.
rx is fed by a single conjunction module whose inputs each cycle independently.
The answer is the LCM of all sub-cycle lengths.
"""
from pathlib import Path
from collections import deque
from math import lcm


def solve(s: str) -> int:
    modules = {}
    for line in s.strip().splitlines():
        left, right = line.split(" -> ")
        dests = [d.strip() for d in right.split(",")]
        if left == "broadcaster":
            modules["broadcaster"] = ("broadcaster", dests)
        else:
            modules[left[1:]] = (left[0], dests)

    ff_state = {}
    conj_memory = {}

    for name, (mod_type, _) in modules.items():
        if mod_type == "%":
            ff_state[name] = False
        elif mod_type == "&":
            conj_memory[name] = {}

    for name, (_, dests) in modules.items():
        for d in dests:
            if d in conj_memory:
                conj_memory[d][name] = False

    rx_feeder = None
    for name, (_, dests) in modules.items():
        if "rx" in dests:
            rx_feeder = name
            break

    if rx_feeder is None:
        return -1

    targets = set(conj_memory[rx_feeder].keys())
    cycle_lengths = {}

    presses = 0
    while True:
        presses += 1
        queue = deque([("button", "broadcaster", False)])
        while queue:
            sender, target, is_high = queue.popleft()

            if target == rx_feeder and is_high and sender in targets:
                if sender not in cycle_lengths:
                    cycle_lengths[sender] = presses
                if len(cycle_lengths) == len(targets):
                    return lcm(*cycle_lengths.values())

            if target not in modules:
                continue
            mod_type, dests = modules[target]

            if mod_type == "broadcaster":
                for d in dests:
                    queue.append((target, d, is_high))
            elif mod_type == "%":
                if not is_high:
                    ff_state[target] = not ff_state[target]
                    for d in dests:
                        queue.append((target, d, ff_state[target]))
            elif mod_type == "&":
                conj_memory[target][sender] = is_high
                send_high = not all(conj_memory[target].values())
                for d in dests:
                    queue.append((target, d, send_high))


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d20_input.txt").read_text()))
