#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 5: Binary Boarding (Part 1)

Boarding passes use binary-space partitioning encoded as characters:
    F = lower half (0), B = upper half (1)  -> 7 chars -> row 0-127
    L = lower half (0), R = upper half (1)  -> 3 chars -> col 0-7

The seat ID is:  row * 8 + column.

The clever insight is that the entire 10-character string is just a binary
number if you treat F/L as '0' and B/R as '1'.  The seat ID formula
(row * 8 + col) falls out naturally since the row occupies the high 7 bits
and the column the low 3 bits.
"""

from pathlib import Path


def seat_id(boarding_pass: str) -> int:
    """Convert a 10-character boarding pass to its numeric seat ID by treating
    it as a 10-bit binary number (F/L -> 0, B/R -> 1)."""
    binary = boarding_pass.replace("F", "0").replace("B", "1") \
                          .replace("L", "0").replace("R", "1")
    return int(binary, 2)


def solve(input_path: str = "advent2020/Day5/d5_input.txt") -> int:
    """Return the highest seat ID on any boarding pass."""
    lines = Path(input_path).read_text().splitlines()
    return max(seat_id(line.strip()) for line in lines if line.strip())


if __name__ == "__main__":
    result = solve()
    print(f"Highest seat ID: {result}")
