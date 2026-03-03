#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 1: Sonar Sweep (Part 2)

Instead of comparing individual measurements, compare three-measurement
sliding-window sums.  Count how many times the window sum increases.

Algorithm
---------
The sliding-window sum of [a, b, c] vs [b, c, d] increases iff d > a,
so we compare elements that are three positions apart — no need to
actually compute the window sums.  O(n) time, O(1) extra space.
"""

from pathlib import Path

from day1 import count_increases


def count_window_increases(depths: list[int], window: int = 3) -> int:
    """Return the number of times a sliding-window sum increases.

    Equivalent to ``count_increases`` on the window sums, but exploits
    the telescoping cancellation: sum_{i+1} > sum_i iff
    depths[i + window] > depths[i].
    """
    return sum(depths[i + window] > depths[i] for i in range(len(depths) - window))


def solve(input_path: str = "advent2021/Day1/d1_input.txt") -> int:
    """Read depth measurements and return the sliding-window increase count."""
    depths = [
        int(line)
        for line in Path(input_path).read_text().splitlines()
        if line.strip()
    ]
    return count_window_increases(depths)


if __name__ == "__main__":
    result = solve()
    print(f"Number of sliding-window increases: {result}")
