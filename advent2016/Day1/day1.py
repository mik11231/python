#!/usr/bin/env python3
"""Advent of Code 2016 Day 1 Part 1: No Time for a Taxicab."""

from pathlib import Path


def solve(s: str) -> int:
    """Return Manhattan distance after following all turn+step instructions."""
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # N,E,S,W
    facing = 0
    x = y = 0
    for tok in s.strip().split(", "):
        turn = tok[0]
        steps = int(tok[1:])
        facing = (facing + (1 if turn == "R" else -1)) % 4
        dx, dy = dirs[facing]
        x += dx * steps
        y += dy * steps
    return abs(x) + abs(y)


if __name__ == "__main__":
    text = Path(__file__).with_name("d1_input.txt").read_text(encoding="utf-8")
    print(solve(text))
