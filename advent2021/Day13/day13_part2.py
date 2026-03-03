#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 13: Transparent Origami (Part 2)

Apply every fold instruction and render the resulting dot pattern as text.
The final pattern typically spells out capital letters (the puzzle answer).

Algorithm
---------
Reuse parsing and folding from Part 1.  After all folds, determine the
bounding box and render a grid of ``#`` (dot present) and ``.`` (empty).
"""

from pathlib import Path

from day13 import parse_input, fold


def render(dots: set[tuple[int, int]]) -> str:
    """Render the dot set as a multi-line string of ``#`` and ``.`` characters."""
    max_x = max(x for x, _ in dots)
    max_y = max(y for _, y in dots)
    lines: list[str] = []
    for y in range(max_y + 1):
        lines.append("".join("#" if (x, y) in dots else "." for x in range(max_x + 1)))
    return "\n".join(lines)


def solve(input_path: str = "advent2021/Day13/d13_input.txt") -> str:
    """Read the dot sheet, apply all folds, and return the rendered pattern."""
    text = Path(input_path).read_text()
    dots, folds = parse_input(text)
    for instruction in folds:
        dots = fold(dots, instruction)
    return render(dots)


if __name__ == "__main__":
    result = solve()
    print("Code after all folds:")
    print(result)
