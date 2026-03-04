#!/usr/bin/env python3
"""Advent of Code 2015 Day 19 — Medicine for Rudolph.

Replacements "A => B". Part 1: count distinct molecules after one replacement.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.parsing import lines


def parse(s: str) -> tuple[list[tuple[str, str]], str]:
    """Return (list of (from, to) replacements, molecule)."""
    rules: list[tuple[str, str]] = []
    molecule = ""
    for line in s.splitlines():
        line = line.strip()
        if not line:
            continue
        if " => " in line:
            a, b = line.split(" => ", 1)
            rules.append((a.strip(), b.strip()))
        else:
            molecule = line  # last non-rule line is the molecule
    return rules, molecule


def solve(s: str) -> int:
    """Return count of distinct molecules after one replacement."""
    rules, molecule = parse(s)
    seen: set[str] = set()
    for src, dst in rules:
        start = 0
        while True:
            i = molecule.find(src, start)
            if i == -1:
                break
            new_mol = molecule[:i] + dst + molecule[i + len(src) :]
            seen.add(new_mol)
            start = i + 1
    return len(seen)


if __name__ == "__main__":
    text = Path(__file__).with_name("d19_input.txt").read_text(encoding="utf-8")
    print(solve(text))
