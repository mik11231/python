#!/usr/bin/env python3
"""Advent of Code 2023 Day 2 Part 2 — Cube Conundrum.

For each game, find the minimum number of cubes of each colour that
would make the game possible. The "power" of a set is red*green*blue.
Return the sum of powers across all games.
"""
import re
from pathlib import Path


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    total = 0
    for line in s.strip().splitlines():
        _, reveals = line.split(": ", 1)
        mins: dict[str, int] = {}
        for pair in re.findall(r"(\d+) (\w+)", reveals):
            count, colour = int(pair[0]), pair[1]
            mins[colour] = max(mins.get(colour, 0), count)
        total += mins.get("red", 0) * mins.get("green", 0) * mins.get("blue", 0)
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d2_input.txt").read_text()))
