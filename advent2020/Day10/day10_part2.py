#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 10: Adapter Array (Part 2)

Count the total number of distinct valid adapter arrangements from the
outlet (0 jolts) to the device (max + 3 jolts), where each step can
differ by at most 3 jolts.

Algorithm
---------
Dynamic programming bottom-up: let ``ways[j]`` be the number of ways to
reach joltage ``j``.  For every adapter in sorted order,
``ways[j] = ways[j-1] + ways[j-2] + ways[j-3]`` (only counting values
that are themselves adapters).  O(n) time after sorting.
"""

from pathlib import Path

from day10 import parse_adapters


def count_arrangements(adapters: list[int]) -> int:
    """Return the number of distinct valid adapter chains."""
    adapter_set = set(adapters)
    ways: dict[int, int] = {0: 1}

    for jolt in adapters[1:]:
        ways[jolt] = sum(ways.get(jolt - d, 0) for d in (1, 2, 3))

    return ways[adapters[-1]]


def solve(input_path: str = "advent2020/Day10/d10_input.txt") -> int:
    """Read adapters and return the number of valid arrangements."""
    adapters = parse_adapters(Path(input_path).read_text())
    return count_arrangements(adapters)


if __name__ == "__main__":
    result = solve()
    print(f"Total distinct adapter arrangements: {result}")
