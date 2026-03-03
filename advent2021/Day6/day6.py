#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 6: Lanternfish (Part 1)

Model an exponentially-growing lanternfish population.  Each fish has an
internal timer (0–8).  Every day the timer decreases by 1.  When it hits 0
the fish resets to 6 **and** spawns a new fish starting at 8.

Count the total number of fish after 80 days.

Algorithm
---------
Instead of tracking individual fish (exponential memory), maintain an array
of 9 counts — one per timer value.  Each day, rotate the counts left: fish
at timer 0 become the new spawns (timer 8) **and** reset to timer 6.
O(days) time, O(1) space.
"""

from pathlib import Path


def simulate_lanternfish(counts: list[int], days: int) -> int:
    """Simulate the lanternfish population and return the total after *days*.

    *counts* is a 9-element list where ``counts[i]`` is the number of fish
    with internal timer ``i``.
    """
    c = list(counts)
    for _ in range(days):
        spawning = c[0]
        c[0:8] = c[1:9]
        c[8] = spawning
        c[6] += spawning
    return sum(c)


def _parse_initial(text: str) -> list[int]:
    """Parse comma-separated timer values into a 9-element count array."""
    counts = [0] * 9
    for val in text.strip().split(","):
        counts[int(val)] += 1
    return counts


def solve(input_path: str = "advent2021/Day6/d6_input.txt") -> int:
    """Read initial timers and return the fish count after 80 days."""
    counts = _parse_initial(Path(input_path).read_text())
    return simulate_lanternfish(counts, 80)


if __name__ == "__main__":
    result = solve()
    print(f"Fish after 80 days: {result}")
