#!/usr/bin/env python3
"""Tests for Day 13 using the example from the problem statement.

Four claw machines. Machines 1 and 3 are winnable (costs 280 and 200).
Part 1: total = 480.  Part 2: different machines become winnable with offset.
"""

from day13 import solve as solve_p1
from day13_part2 import solve as solve_p2

EXAMPLE = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""


def test_part1():
    assert solve_p1(EXAMPLE) == 480


def test_part2_runs():
    result = solve_p2(EXAMPLE)
    assert result > 0


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 480")
    test_part2_runs()
    print("PASS  Part 2: runs OK")
    print("\nAll Day 13 tests passed!")
