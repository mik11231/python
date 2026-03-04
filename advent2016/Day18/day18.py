#!/usr/bin/env python3
"""Advent of Code 2016 Day 18 Part 1: Like a Rogue."""

from pathlib import Path


def next_row(row: str) -> str:
    """Generate next tile row based on trap rules."""
    n = len(row)
    out: list[str] = []
    for i in range(n):
        l = row[i - 1] if i > 0 else "."
        c = row[i]
        r = row[i + 1] if i + 1 < n else "."
        trap = (l == "^" and c == "^" and r == ".") or (
            l == "." and c == "^" and r == "^"
        ) or (l == "^" and c == "." and r == ".") or (l == "." and c == "." and r == "^")
        out.append("^" if trap else ".")
    return "".join(out)


def count_safe(seed: str, rows: int) -> int:
    """Count safe tiles in first rows rows."""
    row = seed
    total = row.count(".")
    for _ in range(rows - 1):
        row = next_row(row)
        total += row.count(".")
    return total


def solve(s: str) -> int:
    """Return safe tile count after 40 rows."""
    return count_safe(s.strip(), 40)


if __name__ == "__main__":
    text = Path(__file__).with_name("d18_input.txt").read_text(encoding="utf-8")
    print(solve(text))
