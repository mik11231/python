#!/usr/bin/env python3
"""Advent of Code 2017 Day 20 Part 1."""

from pathlib import Path
import re


PAT = re.compile(r"-?\d+")


def solve(s: str) -> int:
    best = None
    best_i = -1
    for i, ln in enumerate(s.splitlines()):
        x = list(map(int, PAT.findall(ln)))
        p = abs(x[0]) + abs(x[1]) + abs(x[2])
        v = abs(x[3]) + abs(x[4]) + abs(x[5])
        a = abs(x[6]) + abs(x[7]) + abs(x[8])
        key = (a, v, p, i)
        if best is None or key < best:
            best = key
            best_i = i
    return best_i


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d20_input.txt").read_text(encoding="utf-8")))
