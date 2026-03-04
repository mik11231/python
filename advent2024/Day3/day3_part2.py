#!/usr/bin/env python3
"""Advent of Code 2024 Day 3 Part 2 — Mull It Over (do/don't).

Like Part 1, but do() enables and don't() disables future mul instructions.
Multiplications are enabled at the start. Scan left-to-right, toggling state.
"""
import re
from pathlib import Path


def solve(s: str) -> int:
    """Return the sum of enabled mul(X,Y) products."""
    total = 0
    enabled = True
    for m in re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)", s):
        tok = m.group()
        if tok == "do()":
            enabled = True
        elif tok == "don't()":
            enabled = False
        elif enabled:
            total += int(m.group(1)) * int(m.group(2))
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d3_input.txt").read_text()))
