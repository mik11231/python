#!/usr/bin/env python3
"""Advent of Code 2023 Day 5 Part 1 — If You Give A Seed A Fertilizer.

Parse seed numbers and a chain of range-mapping tables. Map each seed
through every table in order (seed->soil->...->location). Return the
lowest final location number.
"""
from pathlib import Path


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    blocks = s.strip().split("\n\n")
    seeds = list(map(int, blocks[0].split(": ")[1].split()))

    maps: list[list[tuple[int, int, int]]] = []
    for block in blocks[1:]:
        lines = block.splitlines()[1:]
        ranges = []
        for line in lines:
            dst, src, length = map(int, line.split())
            ranges.append((dst, src, length))
        maps.append(ranges)

    best = float("inf")
    for val in seeds:
        for mapping in maps:
            for dst, src, length in mapping:
                if src <= val < src + length:
                    val = dst + (val - src)
                    break
        best = min(best, val)
    return int(best)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d5_input.txt").read_text()))
