#!/usr/bin/env python3
"""Tests for Day 6 using the examples from the problem statement."""

from day6 import solve as solve_p1
from day6_part2 import solve as solve_p2

EXAMPLE = """\
Time:      7  15   30
Distance:  9  40  200
"""


def test_part1():
    assert solve_p1(EXAMPLE) == 288


def test_part2():
    assert solve_p2(EXAMPLE) == 71503


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 288")
    test_part2()
    print("PASS  Part 2: 71503")
    print("\nAll Day 6 tests passed!")
