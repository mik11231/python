#!/usr/bin/env python3
"""Advent of Code 2015 Day 17 — No Such Thing as Too Much.

Count subsets of container capacities that sum to eggnog total (150).
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
    """Return count of subsets that sum to 150."""
    caps = parse(s)
    count = 0

    def recurse(i: int, total: int) -> None:
        nonlocal count
        if total == EGGNOG:
            count += 1
            return
        if total > EGGNOG or i >= len(caps):
            return
        recurse(i + 1, total)
        recurse(i + 1, total + caps[i])

    recurse(0, 0)
    return count


if __name__ == "__main__":
    text = Path(__file__).with_name("d17_input.txt").read_text(encoding="utf-8")
    print(solve(text))
