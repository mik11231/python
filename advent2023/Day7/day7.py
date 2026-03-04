#!/usr/bin/env python3
"""Advent of Code 2023 Day 7 Part 1 — Camel Cards.

Rank poker-like hands by type (five-of-a-kind > four-of-a-kind > ... >
high card), breaking ties by comparing cards left-to-right using the
strength order A K Q J T 9 8 7 6 5 4 3 2. Total winnings = sum of
(rank * bid) for each hand.
"""
from collections import Counter
from pathlib import Path

CARD_STRENGTH = {c: i for i, c in enumerate("23456789TJQKA")}


def hand_type(cards: str) -> int:
    """
    Run `hand_type` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: cards.
    - Returns the computed result for this stage of the pipeline.
    """
    counts = sorted(Counter(cards).values(), reverse=True)
    if counts[0] == 5:
        return 6
    if counts[0] == 4:
        return 5
    if counts[0] == 3 and counts[1] == 2:
        return 4
    if counts[0] == 3:
        return 3
    if counts[0] == 2 and counts[1] == 2:
        return 2
    if counts[0] == 2:
        return 1
    return 0


def hand_key(hand_bid: tuple[str, int]) -> tuple[int, ...]:
    """
    Run `hand_key` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: hand_bid.
    - Returns the computed result for this stage of the pipeline.
    """
    cards = hand_bid[0]
    return (hand_type(cards),) + tuple(CARD_STRENGTH[c] for c in cards)


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    hands = []
    for line in s.strip().splitlines():
        cards, bid = line.split()
        hands.append((cards, int(bid)))
    hands.sort(key=hand_key)
    return sum(rank * bid for rank, (_, bid) in enumerate(hands, 1))


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d7_input.txt").read_text()))
