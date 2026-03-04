#!/usr/bin/env python3
"""Tests for Day 2 using the example from the problem statement.

Example reports: 7 6 4 2 1 / 1 2 7 8 9 / 9 7 6 2 1 / 1 3 2 4 5 / 8 6 4 4 1 / 1 3 6 7 9

Part 1: 2 safe reports
Part 2: 4 safe reports (with Problem Dampener)
"""

from day2 import solve as solve_p1
from day2_part2 import solve as solve_p2

EXAMPLE = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


def test_part1():
    assert solve_p1(EXAMPLE) == 2


def test_part2():
    assert solve_p2(EXAMPLE) == 4


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 2 safe reports")
    test_part2()
    print("PASS  Part 2: 4 safe reports")
    print("\nAll Day 2 tests passed!")
