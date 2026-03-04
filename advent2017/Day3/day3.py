#!/usr/bin/env python3
"""Advent of Code 2017 Day 3 Part 1."""

from pathlib import Path


def solve(s: str) -> int:
    n = int(s.strip())
    if n == 1:
        return 0
    layer = 0
    while (2 * layer + 1) ** 2 < n:
        layer += 1
    side = 2 * layer
    maxv = (2 * layer + 1) ** 2
    mids = [maxv - layer - side * i for i in range(4)]
    return layer + min(abs(n - m) for m in mids)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d3_input.txt").read_text(encoding="utf-8")))
