#!/usr/bin/env python3
"""Advent of Code 2016 Day 8 Part 1: Two-Factor Authentication."""

from pathlib import Path


ROWS = 6
COLS = 50


def run(s: str) -> list[list[bool]]:
    """Execute display instructions and return final screen state."""
    g = [[False] * COLS for _ in range(ROWS)]
    for line in s.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("rect "):
            a, b = map(int, line[5:].split("x"))
            for r in range(b):
                for c in range(a):
                    g[r][c] = True
        elif line.startswith("rotate row y="):
            left, by = line.split(" by ")
            r = int(left.split("=")[1])
            k = int(by) % COLS
            g[r] = g[r][-k:] + g[r][:-k]
        elif line.startswith("rotate column x="):
            left, by = line.split(" by ")
            c = int(left.split("=")[1])
            k = int(by) % ROWS
            col = [g[r][c] for r in range(ROWS)]
            col = col[-k:] + col[:-k]
            for r in range(ROWS):
                g[r][c] = col[r]
    return g


def solve(s: str) -> int:
    """Return number of lit pixels."""
    g = run(s)
    return sum(1 for r in range(ROWS) for c in range(COLS) if g[r][c])


if __name__ == "__main__":
    text = Path(__file__).with_name("d8_input.txt").read_text(encoding="utf-8")
    print(solve(text))
