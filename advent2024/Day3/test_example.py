#!/usr/bin/env python3
"""Tests for Day 3 using the examples from the problem statement.

Part 1 example: xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
  → 2*4 + 5*5 + 11*8 + 8*5 = 161

Part 2 example: xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()_mul(8,5))
  → 2*4 + 8*5 = 48
"""

from day3 import solve as solve_p1
from day3_part2 import solve as solve_p2

EXAMPLE_P1 = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
EXAMPLE_P2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()_mul(8,5))"


def test_part1():
    assert solve_p1(EXAMPLE_P1) == 161


def test_part2():
    assert solve_p2(EXAMPLE_P2) == 48


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 161")
    test_part2()
    print("PASS  Part 2: 48")
    print("\nAll Day 3 tests passed!")
