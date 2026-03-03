#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 3: Binary Diagnostic (Part 2)

Determine the *life support rating* by finding the oxygen generator rating
and CO₂ scrubber rating.

Algorithm
---------
For each bit position (left to right), filter the candidate list:
  - Oxygen: keep numbers whose bit matches the *most common* bit at that
    position (prefer '1' on tie).
  - CO₂: keep numbers whose bit matches the *least common* bit at that
    position (prefer '0' on tie).
Stop when one number remains.  O(n × b) worst-case.
"""

from pathlib import Path


def filter_by_bit_criteria(numbers: list[str], *, prefer_most: bool) -> str:
    """Repeatedly filter *numbers* by bit criteria until one remains.

    *prefer_most=True* keeps the most-common-bit matches (oxygen).
    *prefer_most=False* keeps the least-common-bit matches (CO₂).
    """
    candidates = list(numbers)
    width = len(candidates[0])
    for col in range(width):
        if len(candidates) == 1:
            break
        ones = sum(1 for num in candidates if num[col] == "1")
        zeros = len(candidates) - ones
        if prefer_most:
            keep = "1" if ones >= zeros else "0"
        else:
            keep = "0" if zeros <= ones else "1"
        candidates = [num for num in candidates if num[col] == keep]
    return candidates[0]


def life_support_rating(numbers: list[str]) -> tuple[int, int, int]:
    """Return (oxygen, co2, oxygen * co2)."""
    oxygen = int(filter_by_bit_criteria(numbers, prefer_most=True), 2)
    co2 = int(filter_by_bit_criteria(numbers, prefer_most=False), 2)
    return oxygen, co2, oxygen * co2


def solve(input_path: str = "advent2021/Day3/d3_input.txt") -> int:
    """Read the diagnostic report and return the life support rating."""
    numbers = [
        line.strip()
        for line in Path(input_path).read_text().splitlines()
        if line.strip()
    ]
    _, _, product = life_support_rating(numbers)
    return product


if __name__ == "__main__":
    result = solve()
    print(f"Life support rating: {result}")
