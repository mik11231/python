#!/usr/bin/env python3
"""Tests for Day 21 using the example from the problem statement.

Players start at positions 4 and 8.

Part 1: Player 2 loses with 745 points after 993 rolls -> 745 * 993 = 739785.
Part 2: Player 1 wins in 444356092776315 universes (max of both players).
"""

from day21 import parse_input, play_deterministic
from day21_part2 import count_wins

EXAMPLE = """\
Player 1 starting position: 4
Player 2 starting position: 8
"""


def test_parse():
    """Verify starting positions are parsed correctly."""
    p1, p2 = parse_input(EXAMPLE)
    assert (p1, p2) == (4, 8)


def test_part1():
    """Verify Part 1: losing score 745 * 993 rolls = 739785."""
    _, loser_score, total_rolls = play_deterministic(4, 8)
    assert loser_score == 745
    assert total_rolls == 993
    assert loser_score * total_rolls == 739785


def test_part2():
    """Verify Part 2: player 1 wins in 444356092776315 universes."""
    count_wins.cache_clear()
    w1, w2 = count_wins(4, 8, 0, 0, 0)
    assert w1 == 444356092776315
    assert w2 == 341960390180808
    assert max(w1, w2) == 444356092776315


if __name__ == "__main__":
    test_parse()
    print("PASS  Parse: positions (4, 8)")
    test_part1()
    print("PASS  Part 1: 745 * 993 = 739785")
    test_part2()
    print("PASS  Part 2: max wins = 444356092776315")
    print("\nAll Day 21 tests passed!")
