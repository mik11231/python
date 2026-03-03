#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 16: Packet Decoder (Part 2)

Evaluate the BITS expression.  Operator types: 0 = sum, 1 = product,
2 = min, 3 = max, 5 = greater-than, 6 = less-than, 7 = equal-to.
Literal packets (type 4) evaluate to their encoded value.

Algorithm
---------
Reuse the recursive parser from Part 1 which already computes the value
alongside the version sum.
"""

from pathlib import Path

from day16 import hex_to_bits, parse_packet


def solve(input_path: str = "advent2021/Day16/d16_input.txt") -> int:
    """Read the hex-encoded BITS transmission and return the evaluated result."""
    text = Path(input_path).read_text().strip()
    bits = hex_to_bits(text)
    _, _, value = parse_packet(bits, 0)
    return value


if __name__ == "__main__":
    result = solve()
    print(f"Evaluated expression value: {result}")
