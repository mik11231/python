#!/usr/bin/env python3
"""Advent of Code 2024 Day 22 Part 2 - Monkey Market (best change sequence).

For each buyer, compute 2001 prices (last digit of each secret). Track the
first occurrence of each 4-change-diff tuple and sum the corresponding price
across all buyers. Return the maximum total.
"""
from pathlib import Path
from collections import defaultdict
from day22 import evolve


def solve(s: str) -> int:
    totals = defaultdict(int)
    for line in s.strip().splitlines():
        secret = int(line)
        prices = [secret % 10]
        for _ in range(2000):
            secret = evolve(secret)
            prices.append(secret % 10)
        seen = set()
        for i in range(4, len(prices)):
            key = (
                prices[i-3] - prices[i-4],
                prices[i-2] - prices[i-3],
                prices[i-1] - prices[i-2],
                prices[i]   - prices[i-1],
            )
            if key not in seen:
                seen.add(key)
                totals[key] += prices[i]
    return max(totals.values())


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d22_input.txt").read_text()))
