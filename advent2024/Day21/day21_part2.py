#!/usr/bin/env python3
"""Advent of Code 2024 Day 21 Part 2 - Keypad Conundrum (25 robots).

Same approach as Part 1 but with 25 intermediate directional-keypad robots.
The memoized recursion on (button_pair, depth) keeps this tractable despite
the enormous expansion factor.
"""
from pathlib import Path
from day21 import solve as _solve


def solve(s: str) -> int:
    return _solve(s, num_robots=25)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d21_input.txt").read_text()))
