#!/usr/bin/env python3
"""Advent of Code 2016 Day 4 Part 1: Security Through Obscurity."""

from collections import Counter
from pathlib import Path
import re


PAT = re.compile(r"^([a-z-]+)-(\d+)\[([a-z]+)\]$")


def is_real(name: str, checksum: str) -> bool:
    """Return whether the room checksum matches sorted letter frequencies."""
    counts = Counter(ch for ch in name if ch != "-")
    want = "".join(sorted(counts, key=lambda ch: (-counts[ch], ch))[:5])
    return want == checksum


def solve(s: str) -> int:
    """Sum sector IDs of real rooms."""
    total = 0
    for line in s.splitlines():
        m = PAT.match(line.strip())
        if not m:
            continue
        name, sid, chk = m.group(1), int(m.group(2)), m.group(3)
        if is_real(name, chk):
            total += sid
    return total


if __name__ == "__main__":
    text = Path(__file__).with_name("d4_input.txt").read_text(encoding="utf-8")
    print(solve(text))
