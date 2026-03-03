#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 21: Dirac Dice (Part 2)

With a Dirac die every roll splits the universe into three copies (outcomes
1, 2, 3).  Three rolls per turn yield 27 branches, but only 7 distinct
sums (3..9) with known multiplicities.

Algorithm
---------
Memoised recursion on state (pos1, pos2, score1, score2, whose_turn).
Pre-compute the 27-branch distribution {sum: frequency} to collapse
identical branches.  Return the universe count in which the more-winning
player wins.
"""

from collections import Counter
from functools import lru_cache
from itertools import product
from pathlib import Path

from day21 import parse_input

DIRAC_ROLLS: dict[int, int] = Counter(
    a + b + c for a, b, c in product((1, 2, 3), repeat=3)
)


@lru_cache(maxsize=None)
def count_wins(
    pos1: int, pos2: int, score1: int, score2: int, turn: int
) -> tuple[int, int]:
    """Return (player1_wins, player2_wins) from this state onward."""
    if score1 >= 21:
        return (1, 0)
    if score2 >= 21:
        return (0, 1)

    total_w1, total_w2 = 0, 0
    for roll_sum, freq in DIRAC_ROLLS.items():
        if turn == 0:
            new_pos = (pos1 - 1 + roll_sum) % 10 + 1
            w1, w2 = count_wins(new_pos, pos2, score1 + new_pos, score2, 1)
        else:
            new_pos = (pos2 - 1 + roll_sum) % 10 + 1
            w1, w2 = count_wins(pos1, new_pos, score1, score2 + new_pos, 0)
        total_w1 += w1 * freq
        total_w2 += w2 * freq

    return total_w1, total_w2


def solve(input_path: str = "advent2021/Day21/d21_input.txt") -> int:
    """Return the universe count for the player who wins in more universes."""
    text = Path(input_path).read_text()
    p1, p2 = parse_input(text)
    count_wins.cache_clear()
    w1, w2 = count_wins(p1, p2, 0, 0, 0)
    return max(w1, w2)


if __name__ == "__main__":
    print(f"Part 2 answer: {solve()}")
