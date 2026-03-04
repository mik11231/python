#!/usr/bin/env python3
"""Example smoke tests for Day 3."""

from day3 import solve as solve1
from day3_part2 import solve as solve2


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
    assert solve1(">") == 2
    assert solve1("^>v<") == 4
    assert solve1("^v^v^v^v^v") == 2
    assert solve2("^v") == 3
    assert solve2("^>v<") == 3
    assert solve2("^v^v^v^v^v") == 11
    print("Day 3 examples OK")


if __name__ == "__main__":
    main()
