#!/usr/bin/env python3
"""Advent of Code 2015 Day 3 Part 2 — Santa and Robot.

Alternate moves between Santa and Robot; count distinct houses.
"""
from pathlib import Path


def solve(s: str) -> int:
    """Return number of distinct houses visited by Santa and Robot."""
    seen = {(0, 0)}
    pos = [(0, 0), (0, 0)]  # santa, robot
    delta = {"^": (0, 1), "v": (0, -1), ">": (1, 0), "<": (-1, 0)}
    for i, ch in enumerate(s.strip()):
        idx = i % 2
        dx, dy = delta.get(ch, (0, 0))
        x, y = pos[idx]
        x, y = x + dx, y + dy
        pos[idx] = (x, y)
        seen.add((x, y))
    return len(seen)


if __name__ == "__main__":
    text = Path(__file__).with_name("d3_input.txt").read_text(encoding="utf-8")
    print(solve(text))
