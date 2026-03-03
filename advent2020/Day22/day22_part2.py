#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 22: Crab Combat (Part 2) — Recursive Combat

Same as Combat but with two extra rules:
  1. Before each round, if the exact deck configuration has already appeared
     *in this game*, Player 1 wins the game instantly.
  2. If both players have at least as many remaining cards as the value of
     their drawn card, the round winner is decided by a recursive sub-game
     using copies of the next N cards from each deck.  Otherwise the higher
     card wins as before.

Algorithm
---------
Recursion with memoisation via a ``seen`` set of (tuple(d1), tuple(d2)).
Each sub-game gets its own ``seen`` set.
"""

from pathlib import Path

from day22 import parse_decks, score


def play_recursive_combat(deck1: list[int],
                          deck2: list[int]) -> tuple[int, list[int]]:
    """Play Recursive Combat.  Returns ``(winner, winning_deck)``."""
    d1, d2 = list(deck1), list(deck2)
    seen: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()

    while d1 and d2:
        state = (tuple(d1), tuple(d2))
        if state in seen:
            return 1, d1
        seen.add(state)

        c1, c2 = d1.pop(0), d2.pop(0)

        if len(d1) >= c1 and len(d2) >= c2:
            winner, _ = play_recursive_combat(d1[:c1], d2[:c2])
        else:
            winner = 1 if c1 > c2 else 2

        if winner == 1:
            d1.extend((c1, c2))
        else:
            d2.extend((c2, c1))

    return (1, d1) if d1 else (2, d2)


def solve(input_path: str = "advent2020/Day22/d22_input.txt") -> int:
    """Read decks, play Recursive Combat, return the winner's score."""
    text = Path(input_path).read_text()
    deck1, deck2 = parse_decks(text)
    _, winning_deck = play_recursive_combat(deck1, deck2)
    return score(winning_deck)


if __name__ == "__main__":
    result = solve()
    print(f"Winning player's score (Recursive Combat): {result}")
