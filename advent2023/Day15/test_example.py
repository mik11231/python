#!/usr/bin/env python3
"""Tests for Day 15 using the example from the problem statement.

HASH("HASH") = 52.  Sum of all step hashes = 1320.
Part 2 focusing power = 145.
"""

from day15 import solve as solve_p1
from day15_part2 import solve as solve_p2

EXAMPLE = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def test_part1():
    assert solve_p1(EXAMPLE) == 1320


def test_part2():
    assert solve_p2(EXAMPLE) == 145


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 1320")
    test_part2()
    print("PASS  Part 2: 145")
    print("\nAll Day 15 tests passed!")
