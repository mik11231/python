#!/usr/bin/env python3
"""Advent of Code 2015 Day 5 — Doesn't He Have Intern-Elves For This?

Nice: 3+ vowels, at least one double letter, no ab/cd/pq/xy.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.parsing import lines


def solve(s: str) -> int:
    """Count nice strings."""
    bad = ("ab", "cd", "pq", "xy")
    count = 0
    for line in lines(s):
        line = line.strip()
        if not line:
            continue
        vowels = sum(1 for c in line if c in "aeiou")
        if vowels < 3:
            continue
        if any(b in line for b in bad):
            continue
        has_double = any(line[i] == line[i + 1] for i in range(len(line) - 1))
        if has_double:
            count += 1
    return count


if __name__ == "__main__":
    text = Path(__file__).with_name("d5_input.txt").read_text(encoding="utf-8")
    print(solve(text))
