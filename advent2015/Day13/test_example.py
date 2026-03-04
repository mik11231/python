#!/usr/bin/env python3
"""Example smoke tests for Day 13."""

from pathlib import Path

from day13 import solve as solve1
from day13_part2 import solve as solve2


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
    example = """Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol."""
    assert solve1(example) == 330, solve1(example)
    print("Part 1 example: OK")
    # Part 2 with You: one more person, 0 edges for You; max may differ
    r2 = solve2(example)
    assert r2 == 286, r2
    print("Part 2 example: OK")


if __name__ == "__main__":
    main()
