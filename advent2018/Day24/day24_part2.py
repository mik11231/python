"""Advent of Code 2018 solution module."""

from pathlib import Path
from day24 import fight, load


def solve(groups) -> int:
    """Find smallest immune boost that wins without stalemate; return remaining units."""
    boost = 1
    while True:
        winner, units = fight(groups, boost=boost)
        if winner == 'Immune System':
            return units
        boost += 1


if __name__ == '__main__':
    print(solve(load(Path(__file__).with_name('d24_input.txt'))))
