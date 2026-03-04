#!/usr/bin/env python3
"""Advent of Code 2023 Day 20 Part 1 - Pulse Propagation.

Simulate a network of flip-flop and conjunction modules processing pulses.
Press the button 1000 times, count total low and high pulses sent, and
return the product low_count * high_count.
"""
from pathlib import Path
from collections import deque


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

    low_count = 0
    high_count = 0

    for _ in range(1000):
        queue = deque([("button", "broadcaster", False)])
        while queue:
            sender, target, is_high = queue.popleft()
            if is_high:
                high_count += 1
            else:
                low_count += 1

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

    return low_count * high_count


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d20_input.txt").read_text()))
