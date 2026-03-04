#!/usr/bin/env python3
"""Advent of Code 2024 Day 7 Part 1 — Bridge Repair.

For each equation "target: a b c ...", determine if inserting + or * between
the numbers (evaluated left-to-right) can produce the target. Sum all
achievable targets. Uses recursive search with early pruning.
"""
from pathlib import Path


def can_make(target: int, nums: list[int], idx: int, current: int) -> bool:
    if idx == len(nums):
        return current == target
    if current > target:
        return False
    n = nums[idx]
    return (can_make(target, nums, idx + 1, current + n)
            or can_make(target, nums, idx + 1, current * n))


def solve(s: str) -> int:
    """Return the total calibration result for achievable equations."""
    total = 0
    for line in s.strip().splitlines():
        target_s, nums_s = line.split(": ")
        target = int(target_s)
        nums = list(map(int, nums_s.split()))
        if can_make(target, nums, 1, nums[0]):
            total += target
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d7_input.txt").read_text()))
