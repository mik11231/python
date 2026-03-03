#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 20: Trench Map (Part 2)

Same image enhancement as Part 1, but applied 50 times instead of 2.

Algorithm
---------
Reuses ``parse_input`` and ``enhance`` from Part 1.  The infinite-background
toggle is handled automatically by tracking the default pixel each step.
"""

from pathlib import Path

from day20 import enhance, parse_input


def solve(input_path: str = "advent2021/Day20/d20_input.txt") -> int:
    """Enhance the image 50 times and return the number of lit pixels."""
    text = Path(input_path).read_text()
    algorithm, image = parse_input(text)
    default = "."
    for _ in range(50):
        image, default = enhance(image, algorithm, default)
    return len(image)


if __name__ == "__main__":
    print(f"Lit pixels after 50 enhancements: {solve()}")
