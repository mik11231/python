#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 17: Trick Shot (Part 1)

Launch a probe with initial velocity (vx, vy).  Each step the position
updates by velocity, then vx decays toward 0 by 1 and vy decreases by 1
(gravity).  The target area is a rectangular region.

Find the highest y-position the probe can reach while still landing in the
target area.

Algorithm
---------
The y-axis is independent of x.  The probe goes up and returns to y = 0
with downward velocity -(vy + 1).  The next step puts it at y = -(vy + 1).
To just graze the bottom of the target, set -(vy + 1) = y_min, giving
optimal vy = |y_min| - 1.  Maximum height = vy * (vy + 1) / 2.
"""

import re
from pathlib import Path


def parse_target(text: str) -> tuple[int, int, int, int]:
    """Parse 'target area: x=x1..x2, y=y1..y2' and return (x1, x2, y1, y2)."""
    m = re.search(r"x=(-?\d+)\.\.(-?\d+),\s*y=(-?\d+)\.\.(-?\d+)", text)
    if not m:
        raise ValueError(f"Cannot parse target area from: {text!r}")
    return int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))


def solve(input_path: str = "advent2021/Day17/d17_input.txt") -> int:
    """Read the target area and return the maximum reachable y-position."""
    text = Path(input_path).read_text()
    _, _, y1, y2 = parse_target(text)
    y_min = min(y1, y2)
    vy = abs(y_min) - 1
    return vy * (vy + 1) // 2


if __name__ == "__main__":
    result = solve()
    print(f"Highest y position: {result}")
