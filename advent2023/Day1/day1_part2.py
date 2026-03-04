#!/usr/bin/env python3
"""Advent of Code 2023 Day 1 Part 2 — Trebuchet?!

Like Part 1 but spelled-out digits (one, two, ..., nine) also count.
Scan left-to-right for the first digit/word, right-to-left for the last.
Overlapping words like "eightwo" must both be recognised.
"""
from pathlib import Path

WORDS = {
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
    "six": "6", "seven": "7", "eight": "8", "nine": "9",
}
TOKENS = list(WORDS) + list("123456789")


def first_digit(line: str) -> str:
    for i in range(len(line)):
        for tok in TOKENS:
            if line[i:].startswith(tok):
                return WORDS.get(tok, tok)
    raise ValueError(line)


def last_digit(line: str) -> str:
    for i in range(len(line) - 1, -1, -1):
        for tok in TOKENS:
            if line[i:].startswith(tok):
                return WORDS.get(tok, tok)
    raise ValueError(line)


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    total = 0
    for line in s.strip().splitlines():
        total += int(first_digit(line) + last_digit(line))
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d1_input.txt").read_text()))
