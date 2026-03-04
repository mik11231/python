#!/usr/bin/env python3
"""Tests for Day 1 using the example from the problem statement.

Example input:
    3   4 / 4   3 / 2   5 / 1   3 / 3   9 / 3   3

Part 1: total distance = 11
Part 2: similarity score = 31
"""

from day1 import solve as solve_p1
from day1_part2 import solve as solve_p2

EXAMPLE = """\
3   4
4   3
2   5
1   3
3   9
3   3
"""


def test_part1():
    assert solve_p1(EXAMPLE) == 11


def test_part2():
    assert solve_p2(EXAMPLE) == 31


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: total distance = 11")
    test_part2()
    print("PASS  Part 2: similarity score = 31")
    print("\nAll Day 1 tests passed!")
