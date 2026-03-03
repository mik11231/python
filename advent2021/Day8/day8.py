#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 8: Seven Segment Search (Part 1)

Each display line has 10 unique signal patterns and 4 output-value digits.
Digits 1, 4, 7, and 8 use a unique number of segments (2, 4, 3, and 7
respectively), making them immediately identifiable by length alone.

Algorithm
---------
For each line, inspect only the four output values.  Count those whose
length is in {2, 3, 4, 7}.  O(n) where n is the total number of output
digits across all display lines.
"""

from pathlib import Path

UNIQUE_LENGTHS = {2, 3, 4, 7}


def parse_input(text: str) -> list[tuple[list[str], list[str]]]:
    """Parse display notes into ``(patterns, outputs)`` pairs."""
    entries: list[tuple[list[str], list[str]]] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        patterns_part, output_part = line.split(" | ")
        entries.append((patterns_part.split(), output_part.split()))
    return entries


def count_unique_digits(entries: list[tuple[list[str], list[str]]]) -> int:
    """Count output digits whose segment count uniquely identifies them."""
    return sum(
        1
        for _, outputs in entries
        for digit in outputs
        if len(digit) in UNIQUE_LENGTHS
    )


def solve(input_path: str = "advent2021/Day8/d8_input.txt") -> int:
    """Read display notes and return the count of easily-identifiable digits."""
    text = Path(input_path).read_text()
    entries = parse_input(text)
    return count_unique_digits(entries)


if __name__ == "__main__":
    result = solve()
    print(f"Digits 1, 4, 7, 8 appear {result} times in the output values")
