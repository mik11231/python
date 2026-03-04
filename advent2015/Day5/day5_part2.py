#!/usr/bin/env python3
"""Advent of Code 2015 Day 5 Part 2 — Pair twice (non-overlap) and xyx repeat."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.parsing import lines


def solve(s: str) -> int:
    """Count strings with pair repeat and letter repeat with one between."""
    count = 0
    for line in lines(s):
        line = line.strip()
        if not line:
            continue
        pairs: dict[tuple[str, str], list[int]] = {}
        for i in range(len(line) - 1):
            key = (line[i], line[i + 1])
            if key not in pairs:
                pairs[key] = []
            pairs[key].append(i)
        pair_ok = False
        for indices in pairs.values():
            for i in range(len(indices)):
                for j in range(i + 1, len(indices)):
                    if indices[j] - indices[i] >= 2:
                        pair_ok = True
                        break
                if pair_ok:
                    break
            if pair_ok:
                break
        gap_ok = any(
            line[i] == line[i + 2] for i in range(len(line) - 2)
        )
        if pair_ok and gap_ok:
            count += 1
    return count


if __name__ == "__main__":
    text = Path(__file__).with_name("d5_input.txt").read_text(encoding="utf-8")
    print(solve(text))
