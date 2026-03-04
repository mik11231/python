#!/usr/bin/env python3
"""Advent of Code 2023 Day 7 Part 2 — Camel Cards.

J cards are now jokers (wildcards) and individually the weakest card.
Jokers assume whatever label maximises the hand type. We add the joker
count to the most-common non-joker card's count to find the best type.
"""
from collections import Counter
from pathlib import Path

CARD_STRENGTH = {c: i for i, c in enumerate("J23456789TQKA")}


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
    c = Counter(cards)
    jokers = c.pop("J", 0)
    counts = sorted(c.values(), reverse=True) if c else [0]
    counts[0] += jokers
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
