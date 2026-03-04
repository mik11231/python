#!/usr/bin/env python3
"""Advent of Code 2015 Day 13 - Knights of the Dinner Table."""

import itertools
import re
from pathlib import Path


def parse(s: str) -> dict[tuple[str, str], int]:
    """Parse input into happiness deltas. happiness[(a,b)] = units a gains from sitting next to b."""
    happiness: dict[tuple[str, str], int] = {}
    pattern = re.compile(
        r"(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)\."
    )
    for line in s.strip().splitlines():
        m = pattern.match(line.strip())
        if not m:
            continue
        a, sign, n, b = m.groups()
        delta = int(n) if sign == "gain" else -int(n)
        happiness[(a, b)] = delta
    return happiness


def total_happiness(order: list[str], happiness: dict[tuple[str, str], int]) -> int:
    """Total happiness for a circular arrangement."""
    n = len(order)
    total = 0
    for i in range(n):
        a, b = order[i], order[(i + 1) % n]
        total += happiness.get((a, b), 0) + happiness.get((b, a), 0)
    return total


def solve(s: str) -> int:
    """Max total happiness for circular arrangement. Fix one person to break symmetry."""
    happiness = parse(s)
    people = sorted({a for a, _ in happiness.keys()} | {b for _, b in happiness.keys()})
    if not people:
        return 0
    fixed = people[0]
    rest = [p for p in people if p != fixed]
    best = -(10**9)
    for perm in itertools.permutations(rest):
        order = [fixed] + list(perm)
        best = max(best, total_happiness(order, happiness))
    return best


if __name__ == "__main__":
    text = Path(__file__).with_name("d13_input.txt").read_text(encoding="utf-8")
    print(solve(text))
