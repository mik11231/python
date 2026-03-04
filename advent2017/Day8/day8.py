#!/usr/bin/env python3
"""Advent of Code 2017 Day 8 Part 1."""

from collections import defaultdict
from pathlib import Path


OPS = {
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
}


def solve(s: str) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s.
    - Returns the computed result for this stage of the pipeline.
    """
    reg = defaultdict(int)
    for line in s.splitlines():
        r, op, v, _, cr, cmpop, cv = line.split()
        if OPS[cmpop](reg[cr], int(cv)):
            reg[r] += int(v) if op == "inc" else -int(v)
    return max(reg.values()) if reg else 0


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d8_input.txt").read_text(encoding="utf-8")))
