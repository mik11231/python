#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 5: Binary Boarding (Part 2)

Find *your* seat -- the only missing seat ID whose neighbours (ID+1 and ID-1)
both exist in the list.  Since seats at the very front and back of the plane
might not exist, we only look between the observed min and max IDs.

The approach uses set difference: generate the full range of IDs from min to
max, subtract the observed set, and the single remaining ID is ours.
"""

from pathlib import Path

from day5 import seat_id


def solve(input_path: str = "advent2020/Day5/d5_input.txt") -> int:
    """Return the one missing seat ID between the lowest and highest."""
    lines = Path(input_path).read_text().splitlines()
    ids = {seat_id(line.strip()) for line in lines if line.strip()}
    full_range = set(range(min(ids), max(ids) + 1))
    missing = full_range - ids
    if len(missing) != 1:
        raise ValueError(f"Expected exactly 1 missing seat, found {len(missing)}")
    return missing.pop()


if __name__ == "__main__":
    result = solve()
    print(f"Your seat ID: {result}")
