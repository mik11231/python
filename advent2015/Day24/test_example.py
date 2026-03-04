#!/usr/bin/env python3
"""Example smoke tests for Day 24."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from day24 import solve as solve1, parse_weights, min_qe_for_groups
from day24_part2 import solve as solve2


def main() -> None:
    # Example: 1,2,3,4,5,7,8,9,10,11 -> total 60, 3 groups of 20
    # Smallest group 1: e.g. 11+9=20, QE=99. Or 11+8+1=20, QE=88. Or 10+9+1=20, 90. 11+7+2=20, 154. 10+7+3=20, 210. 9+8+3=20, 216. So min QE for size 3 might be 99 (11,9).
    """
    Run `main` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Returns the computed result for this stage of the pipeline.
    """
    example = "1\n2\n3\n4\n5\n7\n8\n9\n10\n11\n"
    weights = parse_weights(example)
    assert sum(weights) == 60
    assert min_qe_for_groups(weights, 3) == 99  # 11+9=20, rest 40 split into 20+20
    assert solve1(example) == 99
    # Part 2: 4 groups of 15. Smallest group: 11+4=15 QE=44 (rest splits into 3x15).
    assert solve2(example) == 44
    print("Day 24 examples OK")


if __name__ == "__main__":
    main()
