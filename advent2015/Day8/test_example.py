#!/usr/bin/env python3
"""Example smoke tests for Day 8."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from day8 import solve as solve1
from day8_part2 import solve as solve2


def main() -> None:
    # "" -> 2-0=2, "abc" -> 5-3=2, "aaa\"aaa" -> 10-7=3, "\x27" -> 6-1=5
    """
    Run `main` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Returns the computed result for this stage of the pipeline.
    """
    assert solve1('""\n') == 2
    assert solve1('"abc"\n') == 2
    assert solve1('"aaa\\"aaa"\n') == 3
    assert solve1('"\\x27"\n') == 5
    assert solve2('""\n') == 4
    assert solve2('"abc"\n') == 4
    assert solve2('"aaa\\"aaa"\n') == 6
    assert solve2('"\\x27"\n') == 5
    print("Day 8 examples OK")


if __name__ == "__main__":
    main()
