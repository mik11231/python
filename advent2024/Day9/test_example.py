#!/usr/bin/env python3
"""Tests for Day 9 using the example from the problem statement.

Disk map "2333133121414131402" expands to 00...111...2...333.44.5555.6666.777.888899.
Part 1 (block compaction): checksum 1928.  Part 2 (whole-file): checksum 2858.
"""

from day9 import solve as solve_p1
from day9_part2 import solve as solve_p2

EXAMPLE = "2333133121414131402"


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
    assert solve_p1(EXAMPLE) == 1928


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
    assert solve_p2(EXAMPLE) == 2858


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 1928")
    test_part2()
    print("PASS  Part 2: 2858")
    print("\nAll Day 9 tests passed!")
