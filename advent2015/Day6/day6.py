#!/usr/bin/env python3
"""Advent of Code 2015 Day 6 — Probably a Fire Hazard.

1000x1000 grid: turn on, turn off, toggle by rectangle. Count lights on.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.parsing import lines, ints


def solve(s: str) -> int:
    """Apply instructions and return number of lights on."""
    grid = [[False] * 1000 for _ in range(1000)]
    for line in lines(s):
        coords = ints(line)
        if len(coords) != 4:
            continue
        x1, y1, x2, y2 = coords
        if "turn on" in line:
            for r in range(y1, y2 + 1):
                for c in range(x1, x2 + 1):
                    grid[r][c] = True
        elif "turn off" in line:
            for r in range(y1, y2 + 1):
                for c in range(x1, x2 + 1):
                    grid[r][c] = False
        elif "toggle" in line:
            for r in range(y1, y2 + 1):
                for c in range(x1, x2 + 1):
                    grid[r][c] = not grid[r][c]
    return sum(1 for row in grid for c in row if c)


if __name__ == "__main__":
    text = Path(__file__).with_name("d6_input.txt").read_text(encoding="utf-8")
    print(solve(text))
