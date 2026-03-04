#!/usr/bin/env python3
"""Example smoke tests for Day 12."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from day12 import solve as solve1
from day12_part2 import solve as solve2


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
    assert solve1("[1,2,3]") == 6
    assert solve1('{"a":2,"b":4}') == 6
    assert solve1("[[[3]]]") == 3
    assert solve1('{"a":{"b":4},"c":-1}') == 3
    assert solve1('{"a":[-1,1]}') == 0
    assert solve1('[-1,{"a":1}]') == 0
    assert solve1('[]') == 0
    assert solve1('{}') == 0
    # Part 2: [1,2,3] -> 6; [1,{"c":"red","b":2},3] -> 4 (skip object with "red")
    assert solve2("[1,2,3]") == 6
    assert solve2('[1,{"c":"red","b":2},3]') == 4
    assert solve2('{"d":"red","e":[1,2,3,4],"f":5}') == 0  # object with red skipped
    assert solve2('[1,"red",5]') == 6  # "red" in array is not an object value
    print("Day 12 examples OK")


if __name__ == "__main__":
    main()
