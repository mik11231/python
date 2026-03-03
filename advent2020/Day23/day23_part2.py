#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 23: Crab Cups (Part 2)

Extend the circle to one million cups (labels max+1 … 1 000 000) and play
ten million moves.  The answer is the product of the two cups immediately
clockwise of cup 1.

Algorithm
---------
Replace the dict with a flat list (``nxt[i]`` = cup clockwise of cup *i*).
List indexing is faster than dict lookup, which matters for 10 million
iterations.
"""

from pathlib import Path

TOTAL_CUPS = 1_000_000
TOTAL_MOVES = 10_000_000


def play_cups_extended(labels: str, total_cups: int = TOTAL_CUPS,
                       moves: int = TOTAL_MOVES) -> list[int]:
    """Play with *total_cups* cups for *moves* rounds.

    Returns a list where ``nxt[i]`` is the cup clockwise of cup *i*.
    """
    cups = [int(c) for c in labels]
    max_label = max(cups)

    nxt = [0] * (total_cups + 1)
    for i in range(len(cups) - 1):
        nxt[cups[i]] = cups[i + 1]

    nxt[cups[-1]] = max_label + 1
    for i in range(max_label + 1, total_cups):
        nxt[i] = i + 1
    nxt[total_cups] = cups[0]

    current = cups[0]
    for _ in range(moves):
        p1 = nxt[current]
        p2 = nxt[p1]
        p3 = nxt[p2]

        nxt[current] = nxt[p3]

        dest = current - 1 or total_cups
        while dest == p1 or dest == p2 or dest == p3:
            dest = dest - 1 or total_cups

        nxt[p3] = nxt[dest]
        nxt[dest] = p1

        current = nxt[current]

    return nxt


def solve(input_path: str = "advent2020/Day23/d23_input.txt") -> int:
    """Read starting cups, extend to 1M, play 10M moves, return product."""
    labels = Path(input_path).read_text().strip()
    nxt = play_cups_extended(labels)
    a = nxt[1]
    b = nxt[a]
    return a * b


if __name__ == "__main__":
    result = solve()
    print(f"Product of two cups after cup 1: {result}")
