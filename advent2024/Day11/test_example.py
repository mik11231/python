#!/usr/bin/env python3
"""Tests for Day 11 using examples from the problem statement.

"125 17" → 22 stones after 6 blinks, 55312 after 25 blinks.
Part 2 uses the same algorithm for 75 blinks (no small example answer given).
"""

from collections import Counter
from day11 import solve as solve_p1, blink
from day11_part2 import solve as solve_p2

EXAMPLE = "125 17"


def test_blink_6():
    assert sum(blink(Counter([125, 17]), 6).values()) == 22


def test_part1():
    assert solve_p1(EXAMPLE) == 55312


def test_part2_runs():
    result = solve_p2(EXAMPLE)
    assert result > 0


if __name__ == "__main__":
    test_blink_6()
    print("PASS  6 blinks: 22")
    test_part1()
    print("PASS  Part 1: 55312")
    test_part2_runs()
    print("PASS  Part 2: runs OK")
    print("\nAll Day 11 tests passed!")
