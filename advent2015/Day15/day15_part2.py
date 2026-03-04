#!/usr/bin/env python3
"""Advent of Code 2015 Day 15 Part 2 - Exactly 500 calories."""

import re
from pathlib import Path

TOTAL_TSP = 100
TARGET_CALORIES = 500


def parse(s: str) -> list[tuple[int, int, int, int, int]]:
    """Parse input. Returns list of (capacity, durability, flavor, texture, calories) per tsp."""
    pattern = re.compile(
        r"\w+: capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)"
    )
    ingredients = []
    for line in s.strip().splitlines():
        m = pattern.search(line.strip())
        if not m:
            continue
        ingredients.append(tuple(int(x) for x in m.groups()))
    return ingredients


def partitions(n: int, k: int) -> list[tuple[int, ...]]:
    """All ways to write n as sum of k non-negative integers."""
    if k == 1:
        return [(n,)]
    out = []
    for x in range(n + 1):
        for rest in partitions(n - x, k - 1):
            out.append((x,) + rest)
    return out


def solve(s: str) -> int:
    """Max score with 100 tsp and exactly 500 calories."""
    ingredients = parse(s)
    if not ingredients:
        return 0
    best = 0
    for amounts in partitions(TOTAL_TSP, len(ingredients)):
        cal = sum(amounts[i] * ingredients[i][4] for i in range(len(ingredients)))
        if cal != TARGET_CALORIES:
            continue
        cap = sum(amounts[i] * ingredients[i][0] for i in range(len(ingredients)))
        dur = sum(amounts[i] * ingredients[i][1] for i in range(len(ingredients)))
        flv = sum(amounts[i] * ingredients[i][2] for i in range(len(ingredients)))
        tex = sum(amounts[i] * ingredients[i][3] for i in range(len(ingredients)))
        score = max(0, cap) * max(0, dur) * max(0, flv) * max(0, tex)
        best = max(best, score)
    return best


if __name__ == "__main__":
    text = Path(__file__).with_name("d15_input.txt").read_text(encoding="utf-8")
    print(solve(text))
