#!/usr/bin/env python3
"""Advent of Code 2017 Day 11 Part 2."""

from pathlib import Path


MOV = {
    "n": (0, -1, 1),
    "ne": (1, -1, 0),
    "se": (1, 0, -1),
    "s": (0, 1, -1),
    "sw": (-1, 1, 0),
    "nw": (-1, 0, 1),
}


def dist(x: int, y: int, z: int) -> int:
    return max(abs(x), abs(y), abs(z))


def solve(s: str) -> int:
    x = y = z = 0
    best = 0
    for t in s.strip().split(","):
        dx, dy, dz = MOV[t]
        x += dx
        y += dy
        z += dz
        best = max(best, dist(x, y, z))
    return best


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d11_input.txt").read_text(encoding="utf-8")))
