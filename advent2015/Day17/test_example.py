#!/usr/bin/env python3
"""Example smoke tests for Day 17."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from day17 import solve as solve1
from day17_part2 import solve as solve2


def main() -> None:
    # Example from problem: capacities 20, 15, 10, 5, 5; target 25 -> 4 subsets
    """
    Run `main` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Returns the computed result for this stage of the pipeline.
    """
    inp = "20\n15\n10\n5\n5\n"
    from day17 import parse
    caps = parse(inp)
    count = 0
    def recurse(i, total):
        """
        Run `recurse` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: i, total.
        - Produces side effects required by the caller (output/mutation/control flow).
        """
        nonlocal count
        if total == 25:
            count += 1
            return
        if total > 25 or i >= len(caps):
            return
        recurse(i + 1, total)
        recurse(i + 1, total + caps[i])
    recurse(0, 0)
    assert count == 4, count
    # Part 2: minimal containers for 25 -> min size 2, count 3 (15+10, 20+5, 20+5)
    min_size = None
    min_count = 0
    def recurse2(i, total, used):
        """
        Run `recurse2` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: i, total, used.
        - Produces side effects required by the caller (output/mutation/control flow).
        """
        nonlocal min_size, min_count
        if total == 25:
            if min_size is None or used < min_size:
                min_size = used
                min_count = 1
            elif used == min_size:
                min_count += 1
            return
        if total > 25 or i >= len(caps):
            return
        if min_size is not None and used >= min_size:
            return
        recurse2(i + 1, total, used)
        recurse2(i + 1, total + caps[i], used + 1)
    recurse2(0, 0, 0)
    assert min_size == 2 and min_count == 3, (min_size, min_count)
    print("Day 17 examples OK")


if __name__ == "__main__":
    main()
