#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 24: Arithmetic Logic Unit (Part 2)

Find the *smallest* 14-digit model number accepted by MONAD.

Algorithm
---------
Reuses ``extract_parameters`` and ``solve_monad`` from Part 1, passing
``maximize=False`` to prefer the digit 1 in each constraint pair.
"""

from pathlib import Path

from day24 import extract_parameters, solve_monad


def solve(input_path: str = "advent2021/Day24/d24_input.txt") -> int:
    """Return the smallest accepted 14-digit model number."""
    text = Path(input_path).read_text()
    params = extract_parameters(text)
    return solve_monad(params, maximize=False)


if __name__ == "__main__":
    print(f"Smallest valid model number: {solve()}")
