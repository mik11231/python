#!/usr/bin/env python3
"""Advent of Code 2016 Day 20 Part 2: count allowed addresses."""

from pathlib import Path


MAX_IP = 4294967295


def parse_ranges(s: str) -> list[tuple[int, int]]:
    """Parse low-high blocked ranges."""
    out = []
    for ln in s.splitlines():
        if not ln.strip():
            continue
        a, b = map(int, ln.split("-"))
        out.append((a, b))
    return sorted(out)


def solve(s: str) -> int:
    """Return number of allowed IPs in [0, 4294967295]."""
    ranges = parse_ranges(s)
    cur = 0
    allowed = 0
    for a, b in ranges:
        if a > cur:
            allowed += a - cur
        cur = max(cur, b + 1)
        if cur > MAX_IP:
            return allowed
    if cur <= MAX_IP:
        allowed += MAX_IP - cur + 1
    return allowed


if __name__ == "__main__":
    text = Path(__file__).with_name("d20_input.txt").read_text(encoding="utf-8")
    print(solve(text))
