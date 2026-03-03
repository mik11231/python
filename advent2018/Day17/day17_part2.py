"""Advent of Code 2018 solution module."""

from pathlib import Path
from day17 import load_clay, simulate


def solve(path: Path) -> int:
    clay, min_y, max_y = load_clay(path)
    _, settled = simulate(clay, min_y, max_y)
    return sum(1 for _, y in settled if min_y <= y <= max_y)


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d17_input.txt')))
