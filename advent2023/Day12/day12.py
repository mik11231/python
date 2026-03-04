#!/usr/bin/env python3
"""Advent of Code 2023 Day 12 Part 1 — Hot Springs.

Count valid arrangements of damaged/operational springs matching the given
contiguous-group sizes.  Uses memoized recursive DP over (position in pattern,
position in groups list).
"""
from pathlib import Path
from functools import lru_cache


def count_arrangements(pattern: str, groups: tuple[int, ...]) -> int:
    """Return the number of valid arrangements for one row."""

    @lru_cache(maxsize=None)
    def dp(pi: int, gi: int) -> int:
        if gi == len(groups):
            return 0 if "#" in pattern[pi:] else 1
        if pi >= len(pattern):
            return 0

        result = 0
        ch = pattern[pi]

        if ch in ".?":
            result += dp(pi + 1, gi)

        if ch in "#?":
            g = groups[gi]
            block = pattern[pi : pi + g]
            if (
                len(block) == g
                and "." not in block
                and (pi + g == len(pattern) or pattern[pi + g] != "#")
            ):
                result += dp(pi + g + 1, gi + 1)

        return result

    return dp(0, 0)


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    total = 0
    for line in s.strip().splitlines():
        pattern, nums = line.split()
        groups = tuple(map(int, nums.split(",")))
        total += count_arrangements(pattern, groups)
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d12_input.txt").read_text()))
