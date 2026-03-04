#!/usr/bin/env python3
"""Advent of Code 2015 Day 6 Part 2 — Brightness.

Increase/decrease by 1, toggle +2. Return total brightness.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.parsing import lines, ints


def solve(s: str) -> int:
    """Apply brightness instructions and return sum of all values."""
    grid = [[0] * 1000 for _ in range(1000)]
    for line in lines(s):
        coords = ints(line)
        if len(coords) != 4:
            continue
        x1, y1, x2, y2 = coords
        if "turn on" in line:
            for r in range(y1, y2 + 1):
                for c in range(x1, x2 + 1):
                    grid[r][c] += 1
        elif "turn off" in line:
            for r in range(y1, y2 + 1):
                for c in range(x1, x2 + 1):
                    grid[r][c] = max(0, grid[r][c] - 1)
        elif "toggle" in line:
            for r in range(y1, y2 + 1):
                for c in range(x1, x2 + 1):
                    grid[r][c] += 2
    return sum(c for row in grid for c in row)


if __name__ == "__main__":
    text = Path(__file__).with_name("d6_input.txt").read_text(encoding="utf-8")
    print(solve(text))
