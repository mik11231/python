#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 17: Trick Shot (Part 2)

Count every distinct initial velocity (vx, vy) that causes the probe to
be within the target area at any step.

Algorithm
---------
Brute-force over feasible velocity ranges.  vx ranges from 1 to x_max
(any higher overshoots on the first step).  vy ranges from y_min (the
lowest target edge—any lower overshoots immediately) to |y_min| - 1 (the
Part 1 optimum).  For each candidate, simulate the trajectory until the
probe passes beyond the target.
"""

from pathlib import Path

from day17 import parse_target


def count_valid_velocities(x1: int, x2: int, y1: int, y2: int) -> int:
    """Return the number of distinct (vx, vy) that hit the target rectangle."""
    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)
    count = 0
    for vx0 in range(1, x_max + 1):
        for vy0 in range(y_min, abs(y_min)):
            x, y = 0, 0
            vx, vy = vx0, vy0
            while x <= x_max and y >= y_min:
                if x_min <= x <= x_max and y_min <= y <= y_max:
                    count += 1
                    break
                x += vx
                y += vy
                vx = max(vx - 1, 0)
                vy -= 1
    return count


def solve(input_path: str = "advent2021/Day17/d17_input.txt") -> int:
    """Read the target area and return the count of valid initial velocities."""
    text = Path(input_path).read_text()
    x1, x2, y1, y2 = parse_target(text)
    return count_valid_velocities(x1, x2, y1, y2)


if __name__ == "__main__":
    result = solve()
    print(f"Distinct initial velocities: {result}")
