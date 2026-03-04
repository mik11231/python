#!/usr/bin/env python3
"""Advent of Code 2015 Day 16 - Aunt Sue."""

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


def solve(s: str) -> int:
    """Find Sue number where all listed compounds match ticker tape (exact)."""
    sues = parse(s)
    for sue_num, compounds in sues:
        if all(compounds.get(k) == v for k, v in TICKER.items() if k in compounds):
            return sue_num
    return 0


if __name__ == "__main__":
    text = Path(__file__).with_name("d16_input.txt").read_text(encoding="utf-8")
    print(solve(text))
