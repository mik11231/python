#!/usr/bin/env python3
"""Advent of Code 2024 Day 14 Part 1 - Restroom Redoubt.

Simulate robots moving on a 101x103 grid with wrapping edges.
After 100 seconds, compute the safety factor: the product of
the number of robots in each of the four quadrants (excluding
robots exactly on the middle row/column).
"""
from pathlib import Path
import re


def solve(s: str, width: int = 101, height: int = 103, steps: int = 100) -> int:
    """Return the safety factor after the given number of steps."""
    robots = []
    for line in s.strip().splitlines():
        px, py, vx, vy = map(int, re.findall(r'-?\d+', line))
        robots.append((px, py, vx, vy))

    mx, my = width // 2, height // 2
    q = [0, 0, 0, 0]
    for px, py, vx, vy in robots:
        fx = (px + vx * steps) % width
        fy = (py + vy * steps) % height
        if fx == mx or fy == my:
            continue
        qi = (0 if fx < mx else 1) + (0 if fy < my else 2)
        q[qi] += 1

    return q[0] * q[1] * q[2] * q[3]


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d14_input.txt").read_text()))
