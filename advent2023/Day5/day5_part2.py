#!/usr/bin/env python3
"""Advent of Code 2023 Day 5 Part 2 — If You Give A Seed A Fertilizer.

Now the seed line describes ranges (start, length pairs). Brute-forcing
billions of seeds is infeasible, so we map *intervals* through each table:
split each interval at mapping boundaries, apply the offset to mapped parts,
and pass unmapped parts through unchanged.
"""
from pathlib import Path


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    blocks = s.strip().split("\n\n")
    nums = list(map(int, blocks[0].split(": ")[1].split()))
    intervals: list[tuple[int, int]] = []
    for i in range(0, len(nums), 2):
        intervals.append((nums[i], nums[i] + nums[i + 1]))

    maps: list[list[tuple[int, int, int]]] = []
    for block in blocks[1:]:
        lines = block.splitlines()[1:]
        ranges = []
        for line in lines:
            dst, src, length = map(int, line.split())
            ranges.append((dst, src, length))
        maps.append(ranges)

    for mapping in maps:
        new_intervals: list[tuple[int, int]] = []
        while intervals:
            lo, hi = intervals.pop()
            mapped = False
            for dst, src, length in mapping:
                src_end = src + length
                overlap_lo = max(lo, src)
                overlap_hi = min(hi, src_end)
                if overlap_lo < overlap_hi:
                    offset = dst - src
                    new_intervals.append((overlap_lo + offset, overlap_hi + offset))
                    if lo < overlap_lo:
                        intervals.append((lo, overlap_lo))
                    if overlap_hi < hi:
                        intervals.append((overlap_hi, hi))
                    mapped = True
                    break
            if not mapped:
                new_intervals.append((lo, hi))
        intervals = new_intervals

    return min(lo for lo, _ in intervals)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d5_input.txt").read_text()))
