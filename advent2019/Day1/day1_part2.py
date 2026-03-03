"""Advent of Code 2019 Day 1 Part 2."""

from pathlib import Path


def fuel(mass: int) -> int:
    return mass // 3 - 2


def total_fuel(mass: int) -> int:
    acc = 0
    cur = fuel(mass)
    while cur > 0:
        acc += cur
        cur = fuel(cur)
    return acc


def solve(masses: list[int]) -> int:
    return sum(total_fuel(m) for m in masses)


if __name__ == '__main__':
    masses = [int(x) for x in Path(__file__).with_name('d1_input.txt').read_text().splitlines() if x.strip()]
    print(solve(masses))
