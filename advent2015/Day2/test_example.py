#!/usr/bin/env python3
"""Example smoke tests for Day 2."""

from day2 import solve as solve1
from day2_part2 import solve as solve2


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
    assert solve1("2x3x4\n") == 58
    assert solve1("1x1x10\n") == 43
    assert solve2("2x3x4\n") == 34
    assert solve2("1x1x10\n") == 14
    print("Day 2 examples OK")


if __name__ == "__main__":
    main()
