#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 16: Packet Decoder (Part 1)

Decode a hex-encoded BITS transmission into a hierarchy of packets.
Each packet has a 3-bit version and 3-bit type ID.  Type 4 is a literal
value (encoded as groups of 5 bits).  All other types are operator packets
containing sub-packets, identified either by total bit length (length
type 0) or by sub-packet count (length type 1).  Sum all version numbers.

Algorithm
---------
Recursive descent parser on the bit string.  ``parse_packet`` returns the
bit position after parsing, the cumulative version sum, and the evaluated
value of the packet (value is used in Part 2).
"""

import math
from pathlib import Path


def hex_to_bits(hex_str: str) -> str:
    """Convert a hex string to a binary string (zero-padded to 4 bits per digit)."""
    return "".join(f"{int(ch, 16):04b}" for ch in hex_str.strip())


def parse_packet(bits: str, pos: int) -> tuple[int, int, int]:
    """Parse one packet starting at *pos* in *bits*.

    Returns (new_pos, version_sum, value).
    """
    version = int(bits[pos:pos + 3], 2)
    type_id = int(bits[pos + 3:pos + 6], 2)
    pos += 6
    version_sum = version

    if type_id == 4:
        value = 0
        while True:
            group = bits[pos:pos + 5]
            pos += 5
            value = (value << 4) | int(group[1:], 2)
            if group[0] == "0":
                break
        return pos, version_sum, value

    sub_values: list[int] = []
    length_type = bits[pos]
    pos += 1

    if length_type == "0":
        total_length = int(bits[pos:pos + 15], 2)
        pos += 15
        end = pos + total_length
        while pos < end:
            pos, vs, val = parse_packet(bits, pos)
            version_sum += vs
            sub_values.append(val)
    else:
        num_sub = int(bits[pos:pos + 11], 2)
        pos += 11
        for _ in range(num_sub):
            pos, vs, val = parse_packet(bits, pos)
            version_sum += vs
            sub_values.append(val)

    value = _evaluate(type_id, sub_values)
    return pos, version_sum, value


def _evaluate(type_id: int, sub_values: list[int]) -> int:
    """Evaluate an operator packet given its type and sub-packet values."""
    if type_id == 0:
        return sum(sub_values)
    if type_id == 1:
        return math.prod(sub_values)
    if type_id == 2:
        return min(sub_values)
    if type_id == 3:
        return max(sub_values)
    if type_id == 5:
        return int(sub_values[0] > sub_values[1])
    if type_id == 6:
        return int(sub_values[0] < sub_values[1])
    if type_id == 7:
        return int(sub_values[0] == sub_values[1])
    return 0


def solve(input_path: str = "advent2021/Day16/d16_input.txt") -> int:
    """Read the hex-encoded BITS transmission and return the version sum."""
    text = Path(input_path).read_text().strip()
    bits = hex_to_bits(text)
    _, version_sum, _ = parse_packet(bits, 0)
    return version_sum


if __name__ == "__main__":
    result = solve()
    print(f"Sum of all version numbers: {result}")
