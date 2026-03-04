#!/usr/bin/env python3
"""Example smoke tests for Day 9."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from day9 import solve as solve1
from day9_part2 import solve as solve2

EXAMPLE = """London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
"""


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
    assert solve1(EXAMPLE) == 605  # Dublin -> London -> Belfast = 464+518? No: 605 = 464+141 (Dublin->London->Belfast is 464+518=982; Dublin->Belfast->London = 141+518=659; London->Dublin->Belfast = 464+141=605)
    assert solve2(EXAMPLE) == 982  # London -> Dublin -> Belfast = 464+518 = 982
    print("Day 9 examples OK")


if __name__ == "__main__":
    main()
