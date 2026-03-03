#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 10: Syntax Scoring (Part 1)

Lines consist of nested bracket pairs ``()``, ``[]``, ``{}``, ``<>``.
A *corrupted* line contains an incorrect closing character.  Score each
corrupted line by its first illegal character.

Algorithm
---------
Use a stack.  Push the expected closing bracket for every opener.  On a
closing bracket, pop the stack and check for a match.  If mismatched the
line is corrupted.  Score mapping: ``)`` → 3, ``]`` → 57, ``}`` → 1197,
``>`` → 25137.  O(n × L) where L is line length.
"""

from pathlib import Path

PAIRS = {"(": ")", "[": "]", "{": "}", "<": ">"}
CORRUPTION_SCORES = {")": 3, "]": 57, "}": 1197, ">": 25137}


def find_first_illegal(line: str) -> str | None:
    """Return the first illegal closing character, or ``None`` if not corrupted."""
    stack: list[str] = []
    for ch in line:
        if ch in PAIRS:
            stack.append(PAIRS[ch])
        elif stack and ch == stack[-1]:
            stack.pop()
        else:
            return ch
    return None


def score_corrupted(lines: list[str]) -> int:
    """Return the total syntax error score for all corrupted lines."""
    total = 0
    for line in lines:
        illegal = find_first_illegal(line)
        if illegal is not None:
            total += CORRUPTION_SCORES[illegal]
    return total


def solve(input_path: str = "advent2021/Day10/d10_input.txt") -> int:
    """Read navigation subsystem lines and return the corruption score."""
    text = Path(input_path).read_text()
    lines = [line for line in text.splitlines() if line.strip()]
    return score_corrupted(lines)


if __name__ == "__main__":
    result = solve()
    print(f"Total syntax error score: {result}")
