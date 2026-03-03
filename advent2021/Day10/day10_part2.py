#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 10: Syntax Scoring (Part 2)

Incomplete (non-corrupted) lines have unclosed brackets.  Determine the
closing sequence needed to complete each line and score it.  Return the
middle score from all incomplete lines (there is always an odd count).

Algorithm
---------
After stack-based parsing, lines with a non-empty stack and no corruption
are incomplete.  The completion string is the remaining stack reversed.
Score: start at 0; for each character multiply by 5 then add the character
value (``)`` → 1, ``]`` → 2, ``}`` → 3, ``>`` → 4).
"""

from pathlib import Path

from day10 import find_first_illegal, PAIRS

COMPLETION_SCORES = {")": 1, "]": 2, "}": 3, ">": 4}


def completion_score(line: str) -> int | None:
    """Return the autocomplete score for an incomplete line, or ``None`` if corrupted."""
    stack: list[str] = []
    for ch in line:
        if ch in PAIRS:
            stack.append(PAIRS[ch])
        elif stack and ch == stack[-1]:
            stack.pop()
        else:
            return None

    score = 0
    for ch in reversed(stack):
        score = score * 5 + COMPLETION_SCORES[ch]
    return score


def solve(input_path: str = "advent2021/Day10/d10_input.txt") -> int:
    """Read navigation lines and return the middle autocomplete score."""
    text = Path(input_path).read_text()
    lines = [line for line in text.splitlines() if line.strip()]
    scores = [
        s for line in lines
        if (s := completion_score(line)) is not None
    ]
    scores.sort()
    return scores[len(scores) // 2]


if __name__ == "__main__":
    result = solve()
    print(f"Middle autocomplete score: {result}")
