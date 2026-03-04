#!/usr/bin/env python3
"""Tests for Day 4 using the example from the problem statement.

10x10 grid where XMAS appears 18 times (Part 1) and X-MAS appears 9 times (Part 2).
"""

from day4 import solve as solve_p1
from day4_part2 import solve as solve_p2

EXAMPLE = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""


def test_part1():
    assert solve_p1(EXAMPLE) == 18


def test_part2():
    assert solve_p2(EXAMPLE) == 9


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 18 XMAS occurrences")
    test_part2()
    print("PASS  Part 2: 9 X-MAS patterns")
    print("\nAll Day 4 tests passed!")
