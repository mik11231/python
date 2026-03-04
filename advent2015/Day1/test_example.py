#!/usr/bin/env python3
"""Example smoke tests for Day 1."""

from pathlib import Path

from day1 import solve as solve1
from day1_part2 import solve as solve2


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
    assert solve1("(())") == 0
    assert solve1("()()") == 0
    assert solve1("(((") == 3
    assert solve1("(()(()(") == 3
    assert solve1("))(((((") == 3
    assert solve2(")") == 1
    assert solve2("()())") == 5
    print("Day 1 examples OK")


if __name__ == "__main__":
    main()
