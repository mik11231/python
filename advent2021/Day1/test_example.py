#!/usr/bin/env python3
"""Tests for Day 1 using the example from the problem statement.

Example input (ten depth measurements):
    199, 200, 208, 210, 200, 207, 240, 269, 260, 263

Part 1: 7 measurements are larger than the previous measurement.
Part 2: 5 sliding-window sums are larger than the previous sum.
"""

from day1 import count_increases
from day1_part2 import count_window_increases

EXAMPLE = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]


def test_part1():
    """Verify Part 1: seven individual depth increases."""
    assert count_increases(EXAMPLE) == 7


def test_part2():
    """Verify Part 2: five sliding-window sum increases."""
    assert count_window_increases(EXAMPLE) == 5


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 7 increases")
    test_part2()
    print("PASS  Part 2: 5 sliding-window increases")
    print("\nAll Day 1 tests passed!")
