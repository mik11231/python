#!/usr/bin/env python3
"""Advent of Code 2024 Day 14 Part 2 - Restroom Redoubt.

Find the time step when the robots form a Christmas tree picture.
The tree appears when all robots are at unique positions (no overlaps).
We check each second until we find such a configuration.
"""
from pathlib import Path
import re


def solve(s: str, width: int = 101, height: int = 103) -> int:
    """Return the first second at which robots form the Christmas tree."""
    robots = []
    for line in s.strip().splitlines():
        px, py, vx, vy = map(int, re.findall(r'-?\d+', line))
        robots.append((px, py, vx, vy))

    n = len(robots)
    for t in range(1, width * height + 1):
        positions = set()
        for px, py, vx, vy in robots:
            fx = (px + vx * t) % width
            fy = (py + vy * t) % height
            positions.add((fx, fy))
        if len(positions) == n:
            return t

    return -1


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d14_input.txt").read_text()))
