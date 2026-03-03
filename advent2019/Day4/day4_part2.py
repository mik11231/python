"""Advent of Code 2019 Day 4 Part 2."""

from collections import Counter
from pathlib import Path


def valid(n: int) -> bool:
    s = str(n)
    return list(s) == sorted(s) and 2 in Counter(s).values()


def solve(lo: int, hi: int) -> int:
    return sum(1 for n in range(lo, hi + 1) if valid(n))


if __name__ == '__main__':
    lo, hi = map(int, Path(__file__).with_name('d4_input.txt').read_text().strip().split('-'))
    print(solve(lo, hi))
