#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 23: Crab Cups (Part 1)

A circular list of cups labelled with single digits.  Each move:
  1. Pick up the 3 cups immediately clockwise of the current cup.
  2. Select a destination cup: current label − 1, wrapping around,
     skipping any picked-up cups.
  3. Place the 3 picked-up cups immediately clockwise of the destination.
  4. The new current cup is the one immediately clockwise of the old current.

After 100 moves, report the cup labels clockwise from cup 1 (excluding 1).

Algorithm
---------
Use a dict-based linked list: ``nxt[cup] = next_cup_clockwise``.  Each move
is O(1) pointer surgery.
"""

from pathlib import Path


def play_cups(labels: str, moves: int) -> dict[int, int]:
    """Play the crab-cup game and return the next-cup linked-list dict."""
    cups = [int(c) for c in labels]
    max_cup = max(cups)

    nxt: dict[int, int] = {}
    for i in range(len(cups) - 1):
        nxt[cups[i]] = cups[i + 1]
    nxt[cups[-1]] = cups[0]

    current = cups[0]
    for _ in range(moves):
        p1 = nxt[current]
        p2 = nxt[p1]
        p3 = nxt[p2]
        picked = {p1, p2, p3}

        nxt[current] = nxt[p3]

        dest = current - 1 or max_cup
        while dest in picked:
            dest = dest - 1 or max_cup

        nxt[p3] = nxt[dest]
        nxt[dest] = p1

        current = nxt[current]

    return nxt


def labels_after_one(nxt: dict[int, int]) -> str:
    """Read cup labels clockwise from cup 1, excluding 1 itself."""
    parts: list[str] = []
    cup = nxt[1]
    while cup != 1:
        parts.append(str(cup))
        cup = nxt[cup]
    return "".join(parts)


def solve(input_path: str = "advent2020/Day23/d23_input.txt") -> str:
    """Read the starting cups and return labels after cup 1 (100 moves)."""
    labels = Path(input_path).read_text().strip()
    nxt = play_cups(labels, 100)
    return labels_after_one(nxt)


if __name__ == "__main__":
    result = solve()
    print(f"Labels after cup 1: {result}")
