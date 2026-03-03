#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 9: Encoding Error (Part 2)

Find a contiguous sub-sequence (of at least two elements) in the number list
that sums to the invalid number from Part 1.  The answer is the sum of the
smallest and largest values in that range.

Algorithm
---------
Classic sliding-window / two-pointer approach: maintain a running sum between
indices ``lo`` and ``hi``.  Expand ``hi`` when the sum is too small, advance
``lo`` when too large.  O(n) time.
"""

from pathlib import Path

from day9 import find_invalid


def find_contiguous_range(numbers: list[int], target: int) -> list[int]:
    """Return the contiguous sub-list that sums to *target*."""
    lo = 0
    running_sum = 0

    for hi in range(len(numbers)):
        running_sum += numbers[hi]
        while running_sum > target and lo < hi:
            running_sum -= numbers[lo]
            lo += 1
        if running_sum == target and hi - lo >= 1:
            return numbers[lo : hi + 1]

    raise ValueError("No contiguous range sums to the target")


def solve(input_path: str = "advent2020/Day9/d9_input.txt") -> int:
    """Read the XMAS stream, find the invalid number, locate the contiguous
    range, and return min + max of that range."""
    numbers = [
        int(line)
        for line in Path(input_path).read_text().splitlines()
        if line.strip()
    ]
    target = find_invalid(numbers)
    rng = find_contiguous_range(numbers, target)
    return min(rng) + max(rng)


if __name__ == "__main__":
    result = solve()
    print(f"Encryption weakness (min + max of contiguous range): {result}")
