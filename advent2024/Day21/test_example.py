#!/usr/bin/env python3
"""Tests for Day 21 using the example from the problem statement.

Five codes: 029A, 980A, 179A, 456A, 379A.
Part 1 (2 robots): complexities 68*29 + 60*980 + 68*179 + 64*456 + 64*379 = 126384.
Part 2 (25 robots): just verify it produces a positive integer.
"""

from day21 import solve as solve_p1
from day21_part2 import solve as solve_p2

EXAMPLE = """\
029A
980A
179A
456A
379A
"""


def test_part1():
    assert solve_p1(EXAMPLE) == 126384


def test_part2_runs():
    result = solve_p2(EXAMPLE)
    assert result > 0


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 126384")
    test_part2_runs()
    print("PASS  Part 2: runs OK")
    print("\nAll Day 21 tests passed!")
