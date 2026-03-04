#!/usr/bin/env python3
"""Test Day 10 Part 1 with the example from the problem statement."""

from day10 import parse_machine_line, min_presses


EXAMPLE = [
    "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}",
    "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}",
    "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}",
]


def solve_example() -> int:
    """
    Run `solve_example` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Returns the computed result for this stage of the pipeline.
    """
    total = 0
    for line in EXAMPLE:
        num_lights, target_mask, button_masks = parse_machine_line(line)
        total += min_presses(num_lights, target_mask, button_masks)
    return total


if __name__ == "__main__":
    expected = 7
    actual = solve_example()
    print(f"Example total: {actual} (expected {expected})")
    if actual == expected:
        print("Example test PASSED")
    else:
        print("Example test FAILED")

