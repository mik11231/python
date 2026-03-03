#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 7: The Treachery of Whales (Part 1)

Align crab submarines to a single horizontal position with minimum total fuel.
Each step of movement costs 1 unit of fuel, so the cost to move from position
*a* to *t* is ``|a - t|``.

Algorithm
---------
The position minimising the sum of absolute deviations is the **median**.
Sort the list and pick the middle element.  O(n log n) for the sort.
"""

from pathlib import Path


def min_fuel_linear(positions: list[int]) -> tuple[int, int]:
    """Return (optimal_position, total_fuel) using constant cost per step."""
    sorted_pos = sorted(positions)
    target = sorted_pos[len(sorted_pos) // 2]
    fuel = sum(abs(p - target) for p in positions)
    return target, fuel


def solve(input_path: str = "advent2021/Day7/d7_input.txt") -> int:
    """Read crab positions and return the minimum fuel (linear cost)."""
    positions = [int(x) for x in Path(input_path).read_text().strip().split(",")]
    _, fuel = min_fuel_linear(positions)
    return fuel


if __name__ == "__main__":
    result = solve()
    print(f"Minimum fuel (linear cost): {result}")
