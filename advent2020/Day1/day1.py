#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 1: Report Repair (Part 1)

The Elves in accounting need to fix the expense report.  They need to find
the two entries that sum to 2020 and then multiply those two numbers together.

Algorithm
---------
Use a set-based lookup so each entry is checked in O(1), giving O(n) overall
instead of the O(n^2) brute-force nested loop.
"""

from pathlib import Path


def find_two_entries(entries: list[int], target: int = 2020) -> tuple[int, int] | None:
    """Return the pair of entries that sum to *target*, or None."""
    seen: set[int] = set()
    for value in entries:
        complement = target - value
        if complement in seen:
            return (complement, value)
        seen.add(value)
    return None


def solve(input_path: str = "advent2020/Day1/d1_input.txt") -> int:
    """Read the expense report, find the two entries summing to 2020,
    and return their product."""
    entries = [int(line) for line in Path(input_path).read_text().splitlines() if line.strip()]
    pair = find_two_entries(entries)
    if pair is None:
        raise ValueError("No two entries sum to 2020")
    return pair[0] * pair[1]


if __name__ == "__main__":
    result = solve()
    print(f"Product of the two entries that sum to 2020: {result}")
