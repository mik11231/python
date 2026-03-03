"""Advent of Code 2019 Day 14 Part 2."""

from pathlib import Path
from day14 import ore_for_fuel, parse


def solve(s: str, ore=1_000_000_000_000) -> int:
    rec = parse(s)
    lo, hi = 1, 1
    while ore_for_fuel(rec, hi) <= ore:
        hi *= 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if ore_for_fuel(rec, mid) <= ore:
            lo = mid
        else:
            hi = mid - 1
    return lo


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d14_input.txt').read_text()))
