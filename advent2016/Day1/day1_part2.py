#!/usr/bin/env python3
"""Advent of Code 2016 Day 1 Part 2: first repeated location distance."""

from pathlib import Path


def solve(s: str) -> int:
    """Return Manhattan distance to first location visited twice."""
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    facing = 0
    x = y = 0
    seen: set[tuple[int, int]] = {(0, 0)}
    for tok in s.strip().split(", "):
        turn = tok[0]
        steps = int(tok[1:])
        facing = (facing + (1 if turn == "R" else -1)) % 4
        dx, dy = dirs[facing]
        for _ in range(steps):
            x += dx
            y += dy
            p = (x, y)
            if p in seen:
                return abs(x) + abs(y)
            seen.add(p)
    raise ValueError("No repeated location found")


if __name__ == "__main__":
    text = Path(__file__).with_name("d1_input.txt").read_text(encoding="utf-8")
    print(solve(text))
