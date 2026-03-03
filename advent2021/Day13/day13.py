#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 13: Transparent Origami (Part 1)

A transparent sheet has dots at integer coordinates.  Fold instructions fold
the sheet along horizontal (``y=N``) or vertical (``x=N``) lines.  After
folding, overlapping dots merge.  Count the visible dots after the first fold.

Algorithm
---------
Represent dots as a set of ``(x, y)`` tuples.  For each fold, reflect
coordinates that exceed the fold line: ``new = 2 × fold_value − old``.
Duplicates merge automatically in the set.  O(d) per fold where d is the
number of dots.
"""

from pathlib import Path


def parse_input(text: str) -> tuple[set[tuple[int, int]], list[tuple[str, int]]]:
    """Parse dot coordinates and fold instructions from the puzzle input.

    Returns ``(dots, folds)`` where each fold is an ``(axis, value)`` pair.
    """
    parts = text.split("\n\n")

    dots: set[tuple[int, int]] = set()
    for line in parts[0].splitlines():
        if not line.strip():
            continue
        x, y = line.split(",")
        dots.add((int(x), int(y)))

    folds: list[tuple[str, int]] = []
    for line in parts[1].splitlines():
        if not line.strip():
            continue
        spec = line.split()[-1]
        axis, val = spec.split("=")
        folds.append((axis, int(val)))

    return dots, folds


def fold(dots: set[tuple[int, int]], instruction: tuple[str, int]) -> set[tuple[int, int]]:
    """Apply a single fold instruction and return the new set of dots."""
    axis, value = instruction
    new_dots: set[tuple[int, int]] = set()
    for x, y in dots:
        if axis == "x" and x > value:
            x = 2 * value - x
        elif axis == "y" and y > value:
            y = 2 * value - y
        new_dots.add((x, y))
    return new_dots


def solve(input_path: str = "advent2021/Day13/d13_input.txt") -> int:
    """Read the dot sheet, apply the first fold, and return the dot count."""
    text = Path(input_path).read_text()
    dots, folds = parse_input(text)
    dots = fold(dots, folds[0])
    return len(dots)


if __name__ == "__main__":
    result = solve()
    print(f"Dots visible after first fold: {result}")
