#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 6: Lanternfish (Part 2)

Same simulation as Part 1 but for 256 days.  The count-based approach from
Part 1 handles this effortlessly — no algorithmic change needed.
"""

from pathlib import Path

from day6 import simulate_lanternfish


def _parse_initial(text: str) -> list[int]:
    """Parse comma-separated timer values into a 9-element count array."""
    counts = [0] * 9
    for val in text.strip().split(","):
        counts[int(val)] += 1
    return counts


def solve(input_path: str = "advent2021/Day6/d6_input.txt") -> int:
    """Read initial timers and return the fish count after 256 days."""
    counts = _parse_initial(Path(input_path).read_text())
    return simulate_lanternfish(counts, 256)


if __name__ == "__main__":
    result = solve()
    print(f"Fish after 256 days: {result}")
