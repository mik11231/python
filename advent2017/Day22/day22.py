#!/usr/bin/env python3
"""Advent of Code 2017 Day 22 Part 1."""

from pathlib import Path


def solve(s: str) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s.
    - Returns the computed result for this stage of the pipeline.
    """
    lines = [ln.strip() for ln in s.splitlines() if ln.strip()]
    n = len(lines)
    infected = set()
    off = n // 2
    for r, row in enumerate(lines):
        for c, ch in enumerate(row):
            if ch == "#":
                infected.add((r - off, c - off))

    x = y = 0
    d = 0
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    ans = 0
    for _ in range(10_000):
        if (x, y) in infected:
            d = (d + 1) % 4
            infected.remove((x, y))
        else:
            d = (d - 1) % 4
            infected.add((x, y))
            ans += 1
        dx, dy = dirs[d]
        x += dx
        y += dy
    return ans


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d22_input.txt").read_text(encoding="utf-8")))
