#!/usr/bin/env python3
"""Tests for Day 1 using the examples from the problem statement."""

from day1 import solve as solve_p1
from day1_part2 import solve as solve_p2

EXAMPLE_P1 = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

EXAMPLE_P2 = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""


def test_part1():
    assert solve_p1(EXAMPLE_P1) == 142


def test_part2():
    assert solve_p2(EXAMPLE_P2) == 281


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 142")
    test_part2()
    print("PASS  Part 2: 281")
    print("\nAll Day 1 tests passed!")
