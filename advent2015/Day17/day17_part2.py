#!/usr/bin/env python3
"""Advent of Code 2015 Day 17 Part 2 — Minimum containers.

Minimum number of containers that sum to 150; count how many such combinations.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.parsing import lines


EGGNOG = 150


def parse(s: str) -> list[int]:
    """Return list of container capacities."""
    return [int(line.strip()) for line in lines(s) if line.strip()]


def solve(s: str) -> int:
    """Return count of minimal-size subsets that sum to 150."""
    caps = parse(s)
    min_size: int | None = None
    count = 0

    def recurse(i: int, total: int, used: int) -> None:
        nonlocal min_size, count
        if total == EGGNOG:
            if min_size is None or used < min_size:
                min_size = used
                count = 1
            elif used == min_size:
                count += 1
            return
        if total > EGGNOG or i >= len(caps):
            return
        if min_size is not None and used >= min_size:
            return
        recurse(i + 1, total, used)
        recurse(i + 1, total + caps[i], used + 1)

    recurse(0, 0, 0)
    return count


if __name__ == "__main__":
    text = Path(__file__).with_name("d17_input.txt").read_text(encoding="utf-8")
    print(solve(text))
