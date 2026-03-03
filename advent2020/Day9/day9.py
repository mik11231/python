#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 9: Encoding Error (Part 1)

XMAS is a cypher where, after a preamble of N numbers, every subsequent
number must equal the sum of some pair of the N numbers immediately before
it.  Find the first number that violates this rule.

Algorithm
---------
For each candidate starting at index N, check every pair in the preceding
window of size N.  A set-based complement lookup keeps each window check
at O(N).
"""

from pathlib import Path


def find_invalid(numbers: list[int], preamble: int = 25) -> int:
    """Return the first number (after the preamble) that is NOT the sum of
    any two distinct values in the preceding *preamble*-sized window."""
    for i in range(preamble, len(numbers)):
        target = numbers[i]
        window = set(numbers[i - preamble : i])
        if not any(target - x in window and target - x != x for x in window):
            return target
    raise ValueError("All numbers satisfy the XMAS property")


def solve(input_path: str = "advent2020/Day9/d9_input.txt") -> int:
    """Read the XMAS-encoded stream and return the first invalid number."""
    numbers = [
        int(line)
        for line in Path(input_path).read_text().splitlines()
        if line.strip()
    ]
    return find_invalid(numbers)


if __name__ == "__main__":
    result = solve()
    print(f"First number that is not a valid XMAS sum: {result}")
