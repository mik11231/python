#!/usr/bin/env python3
"""Tests for Day 22 using the example from the problem statement.

Player 1: 9, 2, 6, 3, 1
Player 2: 5, 8, 4, 7, 10

Part 1 (Combat):           Player 2 wins, score 306.
Part 2 (Recursive Combat): Player 2 wins, score 291.
"""

from day22 import parse_decks, play_combat, score
from day22_part2 import play_recursive_combat

EXAMPLE = """\
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
"""


def test_parse():
    """Verify parse_decks correctly parses both players' decks."""
    d1, d2 = parse_decks(EXAMPLE)
    assert d1 == [9, 2, 6, 3, 1]
    assert d2 == [5, 8, 4, 7, 10]
    print("PASS  parse_decks")


def test_part1():
    """Verify Part 1 Combat: Player 2 wins with score 306."""
    d1, d2 = parse_decks(EXAMPLE)
    winner, deck = play_combat(d1, d2)
    assert winner == 2, f"Expected Player 2 to win, got Player {winner}"
    s = score(deck)
    assert s == 306, f"Expected score 306, got {s}"
    print(f"PASS  Part 1: Player {winner} wins with score {s}")


def test_part2():
    """Verify Part 2 Recursive Combat: Player 2 wins with score 291."""
    d1, d2 = parse_decks(EXAMPLE)
    winner, deck = play_recursive_combat(d1, d2)
    assert winner == 2, f"Expected Player 2 to win, got Player {winner}"
    s = score(deck)
    assert s == 291, f"Expected score 291, got {s}"
    print(f"PASS  Part 2: Player {winner} wins with score {s}")


def test_infinite_prevention():
    """Recursive Combat must not loop forever on this crafted input."""
    d1, d2 = [43, 19], [2, 29, 14]
    winner, _ = play_recursive_combat(d1, d2)
    assert winner == 1, "Player 1 should win via the infinite-loop rule"
    print("PASS  infinite-prevention rule triggers correctly")


if __name__ == "__main__":
    test_parse()
    test_part1()
    test_part2()
    test_infinite_prevention()
    print("\nAll Day 22 tests passed!")
