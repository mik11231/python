#!/usr/bin/env python3
"""Advent of Code 2015 Day 16 Part 2 - cats/trees > N; pomeranians/goldfish < N; rest == N."""

import re
from pathlib import Path

TICKER = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}

GREATER_THAN = {"cats", "trees"}
LESS_THAN = {"pomeranians", "goldfish"}


def parse(s: str) -> list[tuple[int, dict[str, int]]]:
    """Parse input. Returns list of (sue_num, {compound: value})."""
    pattern = re.compile(r"Sue (\d+): (.+)")
    sues = []
    for line in s.strip().splitlines():
        m = pattern.match(line.strip())
        if not m:
            continue
        num_str, rest = m.groups()
        sue_num = int(num_str)
        compounds = {}
        for part in rest.split(","):
            part = part.strip()
            name, val = part.split(":")
            compounds[name.strip()] = int(val.strip())
        sues.append((sue_num, compounds))
    return sues


def matches(sue_compounds: dict[str, int]) -> bool:
    """Check if Sue's compounds match ticker with Part 2 rules."""
    for k, sue_val in sue_compounds.items():
        ticker_val = TICKER.get(k)
        if ticker_val is None:
            continue
        if k in GREATER_THAN:
            if sue_val <= ticker_val:
                return False
        elif k in LESS_THAN:
            if sue_val >= ticker_val:
                return False
        else:
            if sue_val != ticker_val:
                return False
    return True


def solve(s: str) -> int:
    """Find Sue number with Part 2 matching rules."""
    sues = parse(s)
    for sue_num, compounds in sues:
        if matches(compounds):
            return sue_num
    return 0


if __name__ == "__main__":
    text = Path(__file__).with_name("d16_input.txt").read_text(encoding="utf-8")
    print(solve(text))
