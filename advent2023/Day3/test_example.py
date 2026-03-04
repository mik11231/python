#!/usr/bin/env python3
"""Tests for Day 3 using the examples from the problem statement."""

from day3 import solve as solve_p1
from day3_part2 import solve as solve_p2

EXAMPLE = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def test_part1():
    assert solve_p1(EXAMPLE) == 4361


def test_part2():
    assert solve_p2(EXAMPLE) == 467835


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 4361")
    test_part2()
    print("PASS  Part 2: 467835")
    print("\nAll Day 3 tests passed!")
