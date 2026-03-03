"""Advent of Code 2019 Day 1 Part 1."""

from pathlib import Path


def fuel(mass: int) -> int:
    return mass // 3 - 2


def solve(masses: list[int]) -> int:
    return sum(fuel(m) for m in masses)


if __name__ == '__main__':
    masses = [int(x) for x in Path(__file__).with_name('d1_input.txt').read_text().splitlines() if x.strip()]
    print(solve(masses))
