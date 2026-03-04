#!/usr/bin/env python3
"""Advent of Code 2015 Day 24 — It Hangs in the Balance.

Pack weights; split into 3 equal groups. Minimize group 1 size, then minimize QE (product).
"""
from pathlib import Path
import sys
from itertools import combinations

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.parsing import lines, ints


def parse_weights(s: str) -> list[int]:
    """Return list of weights (one per line)."""
    return [int(line.strip()) for line in lines(s) if line.strip()]


def can_partition(weights: list[int], target: int, num_groups: int) -> bool:
    """Can weights be partitioned into num_groups subsets each summing to target?"""
    if num_groups == 1:
        return sum(weights) == target
    # Find one subset that sums to target; recurse on rest with num_groups - 1
    n = len(weights)
    for k in range(1, n - num_groups + 2):
        for combo in combinations(weights, k):
            if sum(combo) != target:
                continue
            rest = [w for w in weights if w not in combo]
            if can_partition(rest, target, num_groups - 1):
                return True
    return False


def min_qe_for_groups(weights: list[int], num_groups: int) -> int:
    """Minimize group 1 size, then minimize QE (product) of group 1."""
    total = sum(weights)
    if total % num_groups != 0:
        return -1
    target = total // num_groups
    n = len(weights)
    for size in range(1, n - num_groups + 2):
        best_qe = None
        for combo in combinations(weights, size):
            if sum(combo) != target:
                continue
            rest = [w for w in weights if w not in combo]
            if not can_partition(rest, target, num_groups - 1):
                continue
            qe = 1
            for w in combo:
                qe *= w
            if best_qe is None or qe < best_qe:
                best_qe = qe
        if best_qe is not None:
            return best_qe
    return -1


def solve(s: str) -> int:
    """Return minimal QE for the smallest first group in a 3-way split."""
    weights = parse_weights(s)
    return min_qe_for_groups(weights, 3)


if __name__ == "__main__":
    text = Path(__file__).with_name("d24_input.txt").read_text(encoding="utf-8")
    print(solve(text))
