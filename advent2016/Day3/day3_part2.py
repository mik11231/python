#!/usr/bin/env python3
"""Advent of Code 2016 Day 3 Part 2: triangle validity by columns."""

from pathlib import Path


def valid(a: int, b: int, c: int) -> bool:
    """Return True when side lengths satisfy triangle inequality."""
    x, y, z = sorted((a, b, c))
    return x + y > z


def solve(s: str) -> int:
    """Count valid triangles when reading columns in groups of three rows."""
    rows = [list(map(int, ln.split())) for ln in s.splitlines() if ln.strip()]
    total = 0
    for i in range(0, len(rows), 3):
        a, b, c = rows[i : i + 3]
        for col in range(3):
            total += int(valid(a[col], b[col], c[col]))
    return total


if __name__ == "__main__":
    text = Path(__file__).with_name("d3_input.txt").read_text(encoding="utf-8")
    print(solve(text))
