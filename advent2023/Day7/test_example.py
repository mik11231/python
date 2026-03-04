#!/usr/bin/env python3
"""Tests for Day 7 using the examples from the problem statement."""

from day7 import solve as solve_p1
from day7_part2 import solve as solve_p2

EXAMPLE = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""


def test_part1():
    assert solve_p1(EXAMPLE) == 6440


def test_part2():
    assert solve_p2(EXAMPLE) == 5905


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 6440")
    test_part2()
    print("PASS  Part 2: 5905")
    print("\nAll Day 7 tests passed!")
