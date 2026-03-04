#!/usr/bin/env python3
"""Advent of Code 2023 Day 2 Part 1 — Cube Conundrum.

Determine which games are possible if the bag contains only 12 red,
13 green, and 14 blue cubes. A game is possible if no single reveal
exceeds these limits. Return the sum of IDs of possible games.
"""
import re
from pathlib import Path

LIMITS = {"red": 12, "green": 13, "blue": 14}


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    total = 0
    for line in s.strip().splitlines():
        game_part, reveals = line.split(": ", 1)
        game_id = int(game_part.split()[1])
        possible = True
        for pair in re.findall(r"(\d+) (\w+)", reveals):
            if int(pair[0]) > LIMITS.get(pair[1], 0):
                possible = False
                break
        if possible:
            total += game_id
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d2_input.txt").read_text()))
