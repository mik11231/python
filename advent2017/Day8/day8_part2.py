#!/usr/bin/env python3
"""Advent of Code 2017 Day 8 Part 2."""

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
    reg = defaultdict(int)
    best = 0
    for line in s.splitlines():
        r, op, v, _, cr, cmpop, cv = line.split()
        if OPS[cmpop](reg[cr], int(cv)):
            reg[r] += int(v) if op == "inc" else -int(v)
            best = max(best, reg[r])
    return best


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d8_input.txt").read_text(encoding="utf-8")))
