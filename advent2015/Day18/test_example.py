#!/usr/bin/env python3
"""Example smoke tests for Day 18."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from day18 import parse, step, solve as solve1
from day18_part2 import solve as solve2


def main() -> None:
    # Example 3x3: .#. / ..# / ###
    """
    Run `main` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Returns the computed result for this stage of the pipeline.
    """
    inp = ".#.\n..#\n###\n"
    grid = parse(inp)
    assert len(grid) == 3 and len(grid[0]) == 3
    assert grid[0][1] and grid[1][2] and all(grid[2])
    for _ in range(4):
        grid = step(grid)
    count = sum(1 for row in grid for c in row if c)
    assert count == 4, count  # After 4 steps, 4 lights on in example
    print("Day 18 examples OK")


if __name__ == "__main__":
    main()
