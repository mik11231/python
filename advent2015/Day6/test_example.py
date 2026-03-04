#!/usr/bin/env python3
"""Example smoke tests for Day 6."""

from day6 import solve as solve1
from day6_part2 import solve as solve2


def main() -> None:
    """
    Run `main` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Returns the computed result for this stage of the pipeline.
    """
    assert solve1("turn on 0,0 through 999,999\n") == 1000000
    assert solve1("toggle 0,0 through 999,0\n") == 1000
    assert solve1("turn off 499,499 through 500,500\n") == 0
    assert solve2("turn on 0,0 through 0,0\n") == 1
    assert solve2("toggle 0,0 through 999,999\n") == 2000000
    print("Day 6 examples OK")


if __name__ == "__main__":
    main()
