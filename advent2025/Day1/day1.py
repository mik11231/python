#!/usr/bin/env python3
"""Advent of Code 2025 - Day 1: Secret Entrance"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.runner import print_answer, read_input_for


def solve(s: str) -> int:
    """Solve Day 1 Part 1: Count how many times dial points at 0."""
    rotations = [line.strip() for line in s.splitlines() if line.strip()]

    # Dial starts at 50
    position = 50
    count = 0

    # Process each rotation
    for rotation in rotations:
        direction = rotation[0]  # L or R
        distance = int(rotation[1:])  # The number part

        # Apply rotation
        if direction == 'L':
            position = (position - distance) % 100
        else:  # direction == 'R'
            position = (position + distance) % 100

        # Count if dial points at 0
        if position == 0:
            count += 1

    return count

if __name__ == "__main__":
    print_answer(solve(read_input_for(__file__, "d1_input.txt")), label="The password is")
