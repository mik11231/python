#!/usr/bin/env python3
"""Advent of Code 2024 Day 24 Part 1 - Crossed Wires.

Parse initial wire values and gate definitions, then simulate by evaluating
gates whose inputs are ready until all z-wires have values. Combine z-wire
bits (z00 = LSB) into a decimal number.
"""
from pathlib import Path
from collections import deque


def solve(s: str) -> int:
    sections = s.strip().split('\n\n')
    wires = {}
    for line in sections[0].splitlines():
        name, val = line.split(': ')
        wires[name] = int(val)

    gates = []
    for line in sections[1].splitlines():
        lhs, out = line.split(' -> ')
        a, op, b = lhs.split()
        gates.append((a, op, b, out))

    pending = deque(gates)
    while pending:
        a, op, b, out = pending.popleft()
        if a in wires and b in wires:
            va, vb = wires[a], wires[b]
            if op == 'AND':
                wires[out] = va & vb
            elif op == 'OR':
                wires[out] = va | vb
            else:
                wires[out] = va ^ vb
        else:
            pending.append((a, op, b, out))

    result = 0
    for name, val in wires.items():
        if name.startswith('z') and val:
            result |= 1 << int(name[1:])
    return result


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d24_input.txt").read_text()))
