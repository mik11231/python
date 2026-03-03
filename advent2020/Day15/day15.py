#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 15: Rambunctious Recitation (Part 1)

The Elves play a memory game with these rules:

  1. Players take turns saying numbers, starting with a given list.
  2. On each subsequent turn, consider the *most recently* spoken number:
     - If it was the *first* time that number was spoken, say **0**.
     - Otherwise, say the difference between the current turn number and
       the turn number when it was most recently spoken *before* that.

Find the 2020th number spoken.

Algorithm
---------
Keep a dict mapping each number to the turn it was *last* spoken (before the
current turn).  This gives O(1) lookups per turn and O(n) total time.
"""

from pathlib import Path


def play_game(starting: list[int], target: int) -> int:
    """Play the memory game and return the number spoken on turn *target*."""
    last_spoken: dict[int, int] = {}

    for turn, num in enumerate(starting[:-1], start=1):
        last_spoken[num] = turn

    prev = starting[-1]
    for turn in range(len(starting), target):
        if prev in last_spoken:
            speak = turn - last_spoken[prev]
        else:
            speak = 0
        last_spoken[prev] = turn
        prev = speak

    return prev


def solve(input_path: str = "advent2020/Day15/d15_input.txt") -> int:
    """Read starting numbers and return the 2020th number spoken."""
    text = Path(input_path).read_text().strip()
    starting = [int(n) for n in text.split(",")]
    return play_game(starting, 2020)


if __name__ == "__main__":
    result = solve()
    print(f"The 2020th number spoken: {result}")
