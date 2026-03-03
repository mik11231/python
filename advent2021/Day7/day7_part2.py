#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 7: The Treachery of Whales (Part 2)

Fuel cost is now triangular: moving *n* steps costs n*(n+1)/2.

Algorithm
---------
The optimal position for minimising the sum of triangular costs lies near
the **mean** of the positions.  Check both floor(mean) and ceil(mean) and
take the minimum.  O(n) time.
"""

import math
from pathlib import Path


def _triangular_fuel(positions: list[int], target: int) -> int:
    """Total fuel to align all crabs to *target* using triangular cost."""
    total = 0
    for p in positions:
        d = abs(p - target)
        total += d * (d + 1) // 2
    return total


def min_fuel_triangular(positions: list[int]) -> tuple[int, int]:
    """Return (optimal_position, total_fuel) using triangular cost per step."""
    mean = sum(positions) / len(positions)
    lo = math.floor(mean)
    hi = math.ceil(mean)
    fuel_lo = _triangular_fuel(positions, lo)
    fuel_hi = _triangular_fuel(positions, hi)
    if fuel_lo <= fuel_hi:
        return lo, fuel_lo
    return hi, fuel_hi


def solve(input_path: str = "advent2021/Day7/d7_input.txt") -> int:
    """Read crab positions and return the minimum fuel (triangular cost)."""
    positions = [int(x) for x in Path(input_path).read_text().strip().split(",")]
    _, fuel = min_fuel_triangular(positions)
    return fuel


if __name__ == "__main__":
    result = solve()
    print(f"Minimum fuel (triangular cost): {result}")
