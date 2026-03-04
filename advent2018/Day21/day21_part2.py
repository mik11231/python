"""Advent of Code 2018 solution module."""

from pathlib import Path
from day21 import load_constants, next_value


def solve(path: Path) -> int:
    """Return the last unique halt-check value before the sequence repeats."""
    seed, or_mask, byte_mask, full_mask, mul_const = load_constants(path)

    seen = set()
    last = None
    r1 = 0

    while True:
        r1 = next_value(r1, seed, or_mask, byte_mask, full_mask, mul_const)
        if r1 in seen:
            return last
        seen.add(r1)
        last = r1


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d21_input.txt')))
