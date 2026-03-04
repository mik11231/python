#!/usr/bin/env python3
"""Advent of Code 2016 Day 6 Part 2: least-common column decoding."""

from collections import Counter
from pathlib import Path


def solve(s: str) -> str:
    """Recover message from least common character in each column."""
    rows = [ln.strip() for ln in s.splitlines() if ln.strip()]
    cols = len(rows[0])
    out: list[str] = []
    for c in range(cols):
        cnt = Counter(r[c] for r in rows)
        out.append(sorted(cnt, key=lambda ch: (cnt[ch], ch))[0])
    return "".join(out)


if __name__ == "__main__":
    text = Path(__file__).with_name("d6_input.txt").read_text(encoding="utf-8")
    print(solve(text))
