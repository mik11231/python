#!/usr/bin/env python3
"""Advent of Code 2016 Day 3 Part 1: triangle validity by rows."""

from pathlib import Path


def valid(a: int, b: int, c: int) -> bool:
    """Return True when side lengths satisfy triangle inequality."""
    x, y, z = sorted((a, b, c))
    return x + y > z


def solve(s: str) -> int:
    """Count valid triangles in row-wise input."""
    total = 0
    for line in s.splitlines():
        if not line.strip():
            continue
        a, b, c = map(int, line.split())
        total += int(valid(a, b, c))
    return total


if __name__ == "__main__":
    text = Path(__file__).with_name("d3_input.txt").read_text(encoding="utf-8")
    print(solve(text))
