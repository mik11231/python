#!/usr/bin/env python3
"""Tests for Day 12 using the example from the problem statement.

Individual row counts: 1, 4, 1, 1, 4, 10  =>  sum = 21
Part 2 (unfolded 5x): 525152
"""

from day12 import solve as solve_p1, count_arrangements
from day12_part2 import solve as solve_p2

EXAMPLE = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""


def test_individual_rows():
    """
    Run `test_individual_rows` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    expected = [1, 4, 1, 1, 4, 10]
    for line, exp in zip(EXAMPLE.strip().splitlines(), expected):
        pattern, nums = line.split()
        groups = tuple(map(int, nums.split(",")))
        assert count_arrangements(pattern, groups) == exp


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
    assert solve_p1(EXAMPLE) == 21


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
    assert solve_p2(EXAMPLE) == 525152


if __name__ == "__main__":
    test_individual_rows()
    print("PASS  Individual row counts")
    test_part1()
    print("PASS  Part 1: 21")
    test_part2()
    print("PASS  Part 2: 525152")
    print("\nAll Day 12 tests passed!")
