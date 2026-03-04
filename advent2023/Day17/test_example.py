#!/usr/bin/env python3
"""Tests for Day 17 using the example from the problem statement.

Normal crucible minimum heat loss = 102.
Ultra crucible minimum heat loss = 94.
"""

from day17 import solve as solve_p1
from day17_part2 import solve as solve_p2

EXAMPLE = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

EXAMPLE2 = """\
111111111111
999999999991
999999999991
999999999991
999999999991
"""


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
    assert solve_p1(EXAMPLE) == 102


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
    assert solve_p2(EXAMPLE) == 94


def test_part2_example2():
    """
    Run `test_part2_example2` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    assert solve_p2(EXAMPLE2) == 71


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 102")
    test_part2()
    print("PASS  Part 2: 94")
    test_part2_example2()
    print("PASS  Part 2 (example 2): 71")
    print("\nAll Day 17 tests passed!")
