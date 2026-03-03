#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 18: Snailfish (Part 1)

Snailfish numbers are nested pairs.  Addition concatenates two numbers
inside a new pair and then reduces.  Reduction repeatedly applies:
  - explode: the leftmost pair nested 4+ deep pushes its values outward
    and is replaced by 0.
  - split: the leftmost value >= 10 becomes [floor(n/2), ceil(n/2)].

Magnitude of a pair [a, b] = 3 * mag(a) + 2 * mag(b).

Algorithm
---------
Use a flat list of (value, depth) tuples.  Nesting depth is tracked
explicitly rather than via a tree structure.  Explode and split operate
on list indices, making them O(n).  Addition increments all depths by 1
and concatenates the two lists.
"""

import math
from pathlib import Path


def parse_snailfish(line: str) -> list[tuple[int, int]]:
    """Parse a snailfish number string into a flat list of (value, depth)."""
    result: list[tuple[int, int]] = []
    depth = 0
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
        elif ch.isdigit():
            j = i
            while j < len(line) and line[j].isdigit():
                j += 1
            result.append((int(line[i:j]), depth))
            i = j
            continue
        i += 1
    return result


def _explode(number: list[tuple[int, int]]) -> bool:
    """Explode the leftmost pair nested 4+ deep.  Returns True if fired."""
    for i in range(len(number) - 1):
        val_l, depth_l = number[i]
        val_r, depth_r = number[i + 1]
        if depth_l >= 5 and depth_l == depth_r:
            if i > 0:
                number[i - 1] = (number[i - 1][0] + val_l, number[i - 1][1])
            if i + 2 < len(number):
                number[i + 2] = (number[i + 2][0] + val_r, number[i + 2][1])
            number[i:i + 2] = [(0, depth_l - 1)]
            return True
    return False


def _split(number: list[tuple[int, int]]) -> bool:
    """Split the leftmost value >= 10.  Returns True if fired."""
    for i, (val, depth) in enumerate(number):
        if val >= 10:
            number[i:i + 1] = [
                (val // 2, depth + 1),
                (math.ceil(val / 2), depth + 1),
            ]
            return True
    return False


def reduce_number(number: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Fully reduce a snailfish number (explode priority, then split)."""
    while True:
        if _explode(number):
            continue
        if _split(number):
            continue
        break
    return number


def add(a: list[tuple[int, int]], b: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Add two snailfish numbers and reduce the result."""
    combined = [(v, d + 1) for v, d in a] + [(v, d + 1) for v, d in b]
    return reduce_number(combined)


def magnitude(number: list[tuple[int, int]]) -> int:
    """Compute the magnitude of a snailfish number.

    Repeatedly collapse the deepest pair: mag([a, b]) = 3*a + 2*b.
    """
    number = list(number)
    while len(number) > 1:
        max_depth = max(d for _, d in number)
        for i in range(len(number) - 1):
            if number[i][1] == max_depth and number[i + 1][1] == max_depth:
                mag = 3 * number[i][0] + 2 * number[i + 1][0]
                number[i:i + 2] = [(mag, max_depth - 1)]
                break
    return number[0][0]


def solve(input_path: str = "advent2021/Day18/d18_input.txt") -> int:
    """Read snailfish numbers, sum them all, and return the magnitude."""
    lines = Path(input_path).read_text().strip().splitlines()
    numbers = [parse_snailfish(line) for line in lines]
    result = numbers[0]
    for num in numbers[1:]:
        result = add(result, num)
    return magnitude(result)


if __name__ == "__main__":
    result = solve()
    print(f"Magnitude of the final sum: {result}")
