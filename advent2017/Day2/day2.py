#!/usr/bin/env python3
"""Advent of Code 2017 Day 2 Part 1."""

from pathlib import Path


def solve(s: str) -> int:
    total = 0
    for line in s.splitlines():
        if not line.strip():
            continue
        vals = list(map(int, line.split()))
        total += max(vals) - min(vals)
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d2_input.txt").read_text(encoding="utf-8")))
