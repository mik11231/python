#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 22: Crab Combat (Part 1)

Two players play War (Combat) with numbered cards.  Each round, both draw
their top card; the player with the higher card wins and takes both cards
(winner's card first, then loser's) on the bottom of their deck.  The game
ends when a deck is empty.

Score = sum of (card_value × position_from_bottom), 1-indexed.

Algorithm
---------
Use ``collections.deque`` for O(1) popleft.  Play rounds until one deck
is empty, then compute the score.
"""

from collections import deque
from pathlib import Path


def parse_decks(text: str) -> tuple[list[int], list[int]]:
    """Parse the puzzle input into two card lists."""
    p1_block, p2_block = text.strip().split("\n\n")
    deck1 = [int(x) for x in p1_block.splitlines()[1:]]
    deck2 = [int(x) for x in p2_block.splitlines()[1:]]
    return deck1, deck2


def play_combat(deck1: list[int], deck2: list[int]) -> tuple[int, list[int]]:
    """Play a game of Combat.

    Returns ``(winner, winning_deck)`` where *winner* is 1 or 2.
    """
    d1: deque[int] = deque(deck1)
    d2: deque[int] = deque(deck2)
    while d1 and d2:
        c1, c2 = d1.popleft(), d2.popleft()
        if c1 > c2:
            d1.extend((c1, c2))
        else:
            d2.extend((c2, c1))
    return (1, list(d1)) if d1 else (2, list(d2))


def score(deck: list[int]) -> int:
    """Compute the score: card × distance-from-bottom (1-indexed)."""
    return sum(card * (len(deck) - i) for i, card in enumerate(deck))


def solve(input_path: str = "advent2020/Day22/d22_input.txt") -> int:
    """Read decks, play Combat, return the winner's score."""
    text = Path(input_path).read_text()
    deck1, deck2 = parse_decks(text)
    _, winning_deck = play_combat(deck1, deck2)
    return score(winning_deck)


if __name__ == "__main__":
    result = solve()
    print(f"Winning player's score: {result}")
