"""Advent of Code 2019 Day 25 has no separate computational Part 2."""

from pathlib import Path
from day25 import solve


if __name__ == '__main__':
    p = [int(x) for x in Path(__file__).with_name('d25_input.txt').read_text().strip().split(',')]
    print(solve(p))
