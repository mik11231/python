#!/usr/bin/env python3
"""Tests for Day 2 using the example from the problem statement.

Example input:
    1-3 a: abcde      -> valid (sled) / valid (toboggan, pos 1 has 'a')
    1-3 b: cdefg      -> invalid (sled, 0 b's) / invalid (toboggan)
    2-9 c: ccccccccc  -> valid (sled) / invalid (toboggan, both positions)

Part 1 answer: 2 valid
Part 2 answer: 1 valid
"""

from day2 import parse_line, is_valid_sled_policy
from day2_part2 import is_valid_toboggan_policy

EXAMPLE_LINES = [
    "1-3 a: abcde",
    "1-3 b: cdefg",
    "2-9 c: ccccccccc",
]


def test_part1():
    """Verify Part 1: sled policy counts 2 valid passwords in example."""
    results = [is_valid_sled_policy(*parse_line(line)) for line in EXAMPLE_LINES]
    assert results == [True, False, True], f"Expected [True, False, True], got {results}"
    assert sum(results) == 2
    print(f"PASS  Part 1: {sum(results)} valid passwords")


def test_part2():
    """Verify Part 2: toboggan policy counts 1 valid password in example."""
    results = [is_valid_toboggan_policy(*parse_line(line)) for line in EXAMPLE_LINES]
    assert results == [True, False, False], f"Expected [True, False, False], got {results}"
    assert sum(results) == 1
    print(f"PASS  Part 2: {sum(results)} valid passwords")


if __name__ == "__main__":
    test_part1()
    test_part2()
    print("\nAll Day 2 tests passed!")
