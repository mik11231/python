#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 10: Adapter Array (Part 1)

Chain every adapter from the charging outlet (0 jolts) to the device
(max adapter + 3 jolts).  Count the 1-jolt gaps and 3-jolt gaps, then
multiply them together.

Algorithm
---------
Sort the adapters, prepend 0 (outlet) and append max+3 (device), then
count consecutive differences.
"""

from collections import Counter
from pathlib import Path


def parse_adapters(text: str) -> list[int]:
    """Parse newline-separated joltage ratings into a sorted list
    including the outlet (0) and device (max + 3)."""
    adapters = [int(line) for line in text.splitlines() if line.strip()]
    adapters.append(0)
    adapters.append(max(adapters) + 3)
    adapters.sort()
    return adapters


def count_differences(adapters: list[int]) -> Counter[int]:
    """Return a Counter mapping jolt-difference -> count."""
    diffs = [adapters[i + 1] - adapters[i] for i in range(len(adapters) - 1)]
    return Counter(diffs)


def solve(input_path: str = "advent2020/Day10/d10_input.txt") -> int:
    """Read adapters, chain them all, and return
    (# of 1-jolt diffs) * (# of 3-jolt diffs)."""
    adapters = parse_adapters(Path(input_path).read_text())
    diffs = count_differences(adapters)
    return diffs[1] * diffs[3]


if __name__ == "__main__":
    result = solve()
    print(f"Product of 1-jolt and 3-jolt differences: {result}")
