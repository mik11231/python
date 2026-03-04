#!/usr/bin/env python3
"""Advent of Code 2015 Day 20 Part 2 — Elves visit only 50 houses.

Presents = 11 * sum(elf for elf|n and n/elf <= 50) = 11 * sum(d for d in divisors(n) if n//d <= 50).
"""
from pathlib import Path
import math


def divisors(n: int) -> list[int]:
    """Return list of divisors of n."""
    out: list[int] = []
    for d in range(1, int(math.isqrt(n)) + 1):
        if n % d == 0:
            out.append(d)
            if d * d != n:
                out.append(n // d)
    return out


def solve(s: str) -> int:
    """Return first house where 11 * sum(eligible divisors) >= target."""
    target = int(s.strip())
    n = 1
    while True:
        total = 11 * sum(d for d in divisors(n) if n // d <= 50)
        if total >= target:
            return n
        n += 1


if __name__ == "__main__":
    text = Path(__file__).with_name("d20_input.txt").read_text(encoding="utf-8")
    print(solve(text))
