#!/usr/bin/env python3
"""Tests for Day 6 using the example from the problem statement.

Example initial state: 3,4,3,1,2

After  18 days:     26 fish
After  80 days:   5934 fish
After 256 days: 26984457539 fish
"""

from day6 import simulate_lanternfish

INITIAL_COUNTS = [0, 1, 1, 2, 1, 0, 0, 0, 0]
#                  0  1  2  3  4  5  6  7  8  <- timer value
# from input: 3,4,3,1,2 -> one 1, one 2, two 3s, one 4


def test_18_days():
    """Verify 26 fish after 18 days."""
    assert simulate_lanternfish(INITIAL_COUNTS, 18) == 26


def test_part1():
    """Verify Part 1: 5934 fish after 80 days."""
    assert simulate_lanternfish(INITIAL_COUNTS, 80) == 5934


def test_part2():
    """Verify Part 2: 26984457539 fish after 256 days."""
    assert simulate_lanternfish(INITIAL_COUNTS, 256) == 26984457539


if __name__ == "__main__":
    test_18_days()
    print("PASS  18 days: 26 fish")
    test_part1()
    print("PASS  Part 1 (80 days): 5934 fish")
    test_part2()
    print("PASS  Part 2 (256 days): 26984457539 fish")
    print("\nAll Day 6 tests passed!")
