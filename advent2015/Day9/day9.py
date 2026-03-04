#!/usr/bin/env python3
"""Advent of Code 2015 Day 9 — All in a Single Night.

Shortest Hamiltonian path (any order) over cities.
"""
from pathlib import Path
import sys
import itertools

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.parsing import lines


def parse_distances(s: str) -> tuple[set[str], dict[tuple[str, str], int]]:
    """Parse 'X to Y = N' lines; return set of cities and (a,b)->dist (symmetric)."""
    cities: set[str] = set()
    dist: dict[tuple[str, str], int] = {}
    for line in lines(s):
        parts = line.split()
        if len(parts) != 5 or parts[1] != "to" or parts[3] != "=":
            continue
        a, b, n = parts[0], parts[2], int(parts[4])
        cities.add(a)
        cities.add(b)
        dist[(a, b)] = n
        dist[(b, a)] = n
    return cities, dist


def path_length(order: tuple[str, ...], dist: dict[tuple[str, str], int]) -> int:
    """Total distance for visiting cities in order (consecutive pairs)."""
    total = 0
    for i in range(len(order) - 1):
        total += dist[(order[i], order[i + 1])]
    return total


def solve(s: str) -> int:
    """Return shortest total distance for any route visiting each city once."""
    cities, dist = parse_distances(s)
    best = float("inf")
    for perm in itertools.permutations(cities):
        best = min(best, path_length(perm, dist))
    return int(best)


if __name__ == "__main__":
    text = Path(__file__).with_name("d9_input.txt").read_text(encoding="utf-8")
    print(solve(text))
