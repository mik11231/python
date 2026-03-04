#!/usr/bin/env python3
"""Advent of Code 2015 Day 3 — Perfectly Spherical Houses.

Santa moves on 2D grid; count distinct cells visited.
"""
from pathlib import Path


def solve(s: str) -> int:
    """Return number of distinct houses visited."""
    x, y = 0, 0
    seen = {(0, 0)}
    for ch in s.strip():
        if ch == "^":
            y += 1
        elif ch == "v":
            y -= 1
        elif ch == ">":
            x += 1
        elif ch == "<":
            x -= 1
        seen.add((x, y))
    return len(seen)


if __name__ == "__main__":
    text = Path(__file__).with_name("d3_input.txt").read_text(encoding="utf-8")
    print(solve(text))
