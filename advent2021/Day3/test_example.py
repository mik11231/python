#!/usr/bin/env python3
"""Tests for Day 3 using the example from the problem statement.

Example input (12 five-bit binary numbers):
    00100 11110 10110 10111 10101 01111
    00111 11100 10000 11001 00010 01010

Part 1: gamma=22 (10110), epsilon=9 (01001) -> 198
Part 2: oxygen=23 (10111), CO2=10 (01010) -> 230
"""

from day3 import power_consumption
from day3_part2 import life_support_rating

EXAMPLE = [
    "00100", "11110", "10110", "10111", "10101", "01111",
    "00111", "11100", "10000", "11001", "00010", "01010",
]


def test_part1():
    """Verify Part 1: gamma=22, epsilon=9, product=198."""
    gamma, epsilon, product = power_consumption(EXAMPLE)
    assert gamma == 22, f"Expected gamma=22, got {gamma}"
    assert epsilon == 9, f"Expected epsilon=9, got {epsilon}"
    assert product == 198


def test_part2():
    """Verify Part 2: oxygen=23, CO2=10, product=230."""
    oxygen, co2, product = life_support_rating(EXAMPLE)
    assert oxygen == 23, f"Expected oxygen=23, got {oxygen}"
    assert co2 == 10, f"Expected CO2=10, got {co2}"
    assert product == 230


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 198")
    test_part2()
    print("PASS  Part 2: 230")
    print("\nAll Day 3 tests passed!")
