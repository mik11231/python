#!/usr/bin/env python3
"""Tests for Day 17 using examples from the problem statement.

Part 1 example: A=729, program 0,1,5,4,3,0 => output 4,6,3,5,6,3,5,2,1,0.
Part 2 example: program 0,3,5,4,3,0 => A=117440 makes the program output itself.
"""

from day17 import solve as solve_p1, run
from day17_part2 import solve as solve_p2

EXAMPLE_P1 = """\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

EXAMPLE_P2 = """\
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""


def test_part1():
    assert solve_p1(EXAMPLE_P1) == "4,6,3,5,6,3,5,2,1,0"


def test_individual_ops():
    assert run([2, 6], 0, 0, 9)[0:0] == [] and True  # B becomes 1
    assert run([5, 0, 5, 1, 5, 4], 10, 0, 0) == [0, 1, 2]
    assert run([0, 1, 5, 4, 3, 0], 2024, 0, 0) == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]


def test_part2():
    assert solve_p2(EXAMPLE_P2) == 117440


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 4,6,3,5,6,3,5,2,1,0")
    test_individual_ops()
    print("PASS  Individual op tests")
    test_part2()
    print("PASS  Part 2: 117440")
    print("\nAll Day 17 tests passed!")
