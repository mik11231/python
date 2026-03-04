#!/usr/bin/env python3
"""Advent of Code 2023 Day 12 Part 2 — Hot Springs.

Same as Part 1 but each row is unfolded 5 times: the pattern is repeated
5 times separated by '?' and the groups list is repeated 5 times.
"""
from pathlib import Path
from day12 import count_arrangements


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    total = 0
    for line in s.strip().splitlines():
        pattern, nums = line.split()
        groups = tuple(map(int, nums.split(",")))
        pattern = "?".join([pattern] * 5)
        groups = groups * 5
        total += count_arrangements(pattern, groups)
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d12_input.txt").read_text()))
