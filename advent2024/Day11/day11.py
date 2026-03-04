#!/usr/bin/env python3
"""Advent of Code 2024 Day 11 Part 1 - Plutonian Pebbles.

Simulate 25 blinks of stone transformation: 0→1, even-digit stones split,
others multiply by 2024. Uses dict-based counting so identical stones are
processed once regardless of multiplicity.
"""
from pathlib import Path
from collections import Counter


def blink(counts: Counter, times: int) -> Counter:
    """Apply the blink rules *times* times and return final stone counts."""
    for _ in range(times):
        new = Counter()
        for stone, cnt in counts.items():
            if stone == 0:
                new[1] += cnt
            else:
                d = str(stone)
                if len(d) % 2 == 0:
                    mid = len(d) // 2
                    new[int(d[:mid])] += cnt
                    new[int(d[mid:])] += cnt
                else:
                    new[stone * 2024] += cnt
        counts = new
    return counts


def solve(s: str) -> int:
    """Return number of stones after 25 blinks."""
    stones = Counter(map(int, s.strip().split()))
    return sum(blink(stones, 25).values())


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d11_input.txt").read_text()))
