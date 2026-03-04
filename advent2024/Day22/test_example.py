#!/usr/bin/env python3
"""Tests for Day 22 using the examples from the problem statement.

Part 1: buyers 1, 10, 100, 2024 produce 2000th secrets summing to 37327623.
Part 2: buyers 1, 2, 3, 2024, best 4-change sequence yields 23 bananas.
"""

from day22 import solve as solve_p1, evolve
from day22_part2 import solve as solve_p2

EXAMPLE_P1 = """\
1
10
100
2024
"""

EXAMPLE_P2 = """\
1
2
3
2024
"""


def test_evolve_sequence():
    """
    Run `test_evolve_sequence` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    secret = 123
    expected = [15887950, 16495136, 527345, 704524, 1553684,
                12683156, 11100544, 12249484, 7753432, 5908254]
    for e in expected:
        secret = evolve(secret)
        assert secret == e


def test_part1():
    """
    Run `test_part1` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    assert solve_p1(EXAMPLE_P1) == 37327623


def test_part2():
    """
    Run `test_part2` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    assert solve_p2(EXAMPLE_P2) == 23


if __name__ == "__main__":
    test_evolve_sequence()
    print("PASS  evolve sequence")
    test_part1()
    print("PASS  Part 1: 37327623")
    test_part2()
    print("PASS  Part 2: 23")
    print("\nAll Day 22 tests passed!")
