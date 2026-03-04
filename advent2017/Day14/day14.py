#!/usr/bin/env python3
"""Advent of Code 2017 Day 14 Part 1."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from knot import knot_hash


def solve(s: str) -> int:
    key = s.strip()
    total = 0
    for i in range(128):
        h = knot_hash(f"{key}-{i}")
        total += sum(bin(int(c, 16)).count("1") for c in h)
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d14_input.txt").read_text(encoding="utf-8")))
