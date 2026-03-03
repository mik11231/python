#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 21: Dirac Dice (Part 1)

Two players take turns on a circular board (positions 1-10).  A
deterministic 100-sided die is rolled three times per turn.  The player
moves forward by the sum of the three rolls and adds their new position
to their score.  The first player to reach 1000 wins.

Algorithm
---------
Simulate the game directly.  The deterministic die cycles 1..100 so we
track its state with a simple counter mod 100.  The answer is the losing
player's score multiplied by the total number of dice rolls.
"""

import re
from pathlib import Path


def parse_input(text: str) -> tuple[int, int]:
    """Return (player1_start, player2_start) from the puzzle text."""
    nums = re.findall(r"starting position:\s*(\d+)", text)
    return int(nums[0]), int(nums[1])


def play_deterministic(pos1: int, pos2: int) -> tuple[int, int, int]:
    """Simulate the deterministic-die game.

    Returns (winner_score, loser_score, total_rolls).
    """
    scores = [0, 0]
    positions = [pos1, pos2]
    die = 0
    total_rolls = 0

    while True:
        for player in (0, 1):
            roll_sum = 0
            for _ in range(3):
                die = die % 100 + 1
                roll_sum += die
                total_rolls += 1
            positions[player] = (positions[player] - 1 + roll_sum) % 10 + 1
            scores[player] += positions[player]
            if scores[player] >= 1000:
                loser = 1 - player
                return scores[player], scores[loser], total_rolls


def solve(input_path: str = "advent2021/Day21/d21_input.txt") -> int:
    """Return losing_score * total_rolls for the deterministic game."""
    text = Path(input_path).read_text()
    p1, p2 = parse_input(text)
    _, loser_score, total_rolls = play_deterministic(p1, p2)
    return loser_score * total_rolls


if __name__ == "__main__":
    print(f"Part 1 answer: {solve()}")
