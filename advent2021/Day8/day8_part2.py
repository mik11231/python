#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 8: Seven Segment Search (Part 2)

Deduce the full segment mapping for each display line and decode all four
output digits as a four-digit number.  Sum every decoded output value.

Algorithm
---------
1. Identify digits with unique segment counts:
   1 (2 segments), 4 (4), 7 (3), 8 (7).
2. Among the 6-segment digits {0, 6, 9}:
   - 6 does NOT contain all segments of 1.
   - 9 contains all segments of 4.
   - 0 is the remaining 6-segment digit.
3. Among the 5-segment digits {2, 3, 5}:
   - 3 contains all segments of 1.
   - 5 is a subset of 6.
   - 2 is the remaining 5-segment digit.

All set operations are O(1) on 7-element sets, so the overall work is
O(n) in the number of display lines.
"""

from pathlib import Path

from day8 import parse_input


def decode_patterns(patterns: list[str]) -> dict[frozenset[str], int]:
    """Map each signal pattern (as a frozenset of chars) to its digit value."""
    by_len: dict[int, list[frozenset[str]]] = {}
    for p in patterns:
        fs = frozenset(p)
        by_len.setdefault(len(fs), []).append(fs)

    one = by_len[2][0]
    seven = by_len[3][0]
    four = by_len[4][0]
    eight = by_len[7][0]

    six_seg = by_len[6]
    six = next(s for s in six_seg if not one <= s)
    nine = next(s for s in six_seg if four <= s)
    zero = next(s for s in six_seg if s != six and s != nine)

    five_seg = by_len[5]
    three = next(s for s in five_seg if one <= s)
    five = next(s for s in five_seg if s <= six)
    two = next(s for s in five_seg if s != three and s != five)

    return {
        zero: 0, one: 1, two: 2, three: 3, four: 4,
        five: 5, six: 6, seven: 7, eight: 8, nine: 9,
    }


def decode_output(patterns: list[str], outputs: list[str]) -> int:
    """Decode the four output digits into a single integer."""
    mapping = decode_patterns(patterns)
    result = 0
    for digit_str in outputs:
        result = result * 10 + mapping[frozenset(digit_str)]
    return result


def solve(input_path: str = "advent2021/Day8/d8_input.txt") -> int:
    """Read display notes, decode every output, and return their sum."""
    text = Path(input_path).read_text()
    entries = parse_input(text)
    return sum(decode_output(p, o) for p, o in entries)


if __name__ == "__main__":
    result = solve()
    print(f"Sum of all decoded output values: {result}")
