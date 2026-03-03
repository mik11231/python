#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 1: Report Repair (Part 2)

Now find *three* entries in the expense report that sum to 2020 and return
their product.

Algorithm
---------
Sort the list first, then for each element run a two-pointer sweep on the
remainder.  This gives O(n^2) time instead of the O(n^3) brute-force triple
loop, and the early-exit comparison with `highest_possible` (from the
original solution) is preserved via the two-pointer bounds.
"""

from pathlib import Path


def find_three_entries(entries: list[int], target: int = 2020) -> tuple[int, int, int] | None:
    """Return three entries that sum to *target*, or None."""
    nums = sorted(entries)
    length = len(nums)
    for i in range(length - 2):
        left, right = i + 1, length - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == target:
                return (nums[i], nums[left], nums[right])
            elif total < target:
                left += 1
            else:
                right -= 1
    return None


def solve(input_path: str = "advent2020/Day1/d1_input.txt") -> int:
    """Read the expense report, find the three entries summing to 2020,
    and return their product."""
    entries = [int(line) for line in Path(input_path).read_text().splitlines() if line.strip()]
    triplet = find_three_entries(entries)
    if triplet is None:
        raise ValueError("No three entries sum to 2020")
    return triplet[0] * triplet[1] * triplet[2]


if __name__ == "__main__":
    result = solve()
    print(f"Product of the three entries that sum to 2020: {result}")
