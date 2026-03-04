#!/usr/bin/env python3
"""Advent of Code 2024 Day 24 Part 2 - Crossed Wires (find swapped outputs).

The circuit should be a 45-bit ripple-carry adder. Detect the 4 swapped
output pairs by checking structural rules:
  1) z-outputs (except z45) must come from XOR gates
  2) XOR gates with non-x/y inputs must output to a z-wire
  3) XOR gates with x/y inputs (except x00) must feed into another XOR
  4) AND gates with x/y inputs (except x00) must feed into an OR gate
Any wire violating these rules is one of the 8 swapped wires.
"""
from pathlib import Path
from collections import defaultdict


def solve(s: str) -> str:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s.
    - Returns the computed result for this stage of the pipeline.
    """
    sections = s.strip().split('\n\n')
    gates = []
    for line in sections[1].splitlines():
        lhs, out = line.split(' -> ')
        a, op, b = lhs.split()
        gates.append((a, op, b, out))

    feeds_into = defaultdict(set)
    for a, op, b, out in gates:
        feeds_into[a].add(op)
        feeds_into[b].add(op)

    wrong = set()
    for a, op, b, out in gates:
        is_xy = a[0] in 'xy' or b[0] in 'xy'
        is_x00 = 'x00' in (a, b)

        if out.startswith('z') and out != 'z45' and op != 'XOR':
            wrong.add(out)

        if op == 'XOR' and not is_xy and not out.startswith('z'):
            wrong.add(out)

        if op == 'XOR' and is_xy and not is_x00:
            if 'XOR' not in feeds_into.get(out, set()):
                wrong.add(out)

        if op == 'AND' and not is_x00:
            if 'OR' not in feeds_into.get(out, set()):
                wrong.add(out)

    return ','.join(sorted(wrong))


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d24_input.txt").read_text()))
