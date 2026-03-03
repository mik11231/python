#!/usr/bin/env python3
"""Tests for Day 1 using the example from the problem statement.

Example input (five expense-report entries):
    1721, 979, 366, 299, 675, 1456

Part 1: 1721 + 299 = 2020  ->  1721 * 299 = 514579
Part 2: 979 + 366 + 675 = 2020  ->  979 * 366 * 675 = 241861950
"""

from day1 import find_two_entries
from day1_part2 import find_three_entries

EXAMPLE = [1721, 979, 366, 299, 675, 1456]


def test_part1():
    """Verify Part 1: two entries summing to 2020 produce product 514579."""
    pair = find_two_entries(EXAMPLE)
    assert pair is not None, "Expected a pair summing to 2020"
    assert pair[0] * pair[1] == 514579, f"Expected product 514579, got {pair[0] * pair[1]}"
    print(f"PASS  Part 1: {pair[0]} * {pair[1]} = {pair[0] * pair[1]}")


def test_part2():
    """Verify Part 2: three entries summing to 2020 produce product 241861950."""
    triplet = find_three_entries(EXAMPLE)
    assert triplet is not None, "Expected a triplet summing to 2020"
    product = triplet[0] * triplet[1] * triplet[2]
    assert product == 241861950, f"Expected product 241861950, got {product}"
    print(f"PASS  Part 2: {triplet[0]} * {triplet[1]} * {triplet[2]} = {product}")


if __name__ == "__main__":
    test_part1()
    test_part2()
    print("\nAll Day 1 tests passed!")
