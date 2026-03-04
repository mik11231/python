#!/usr/bin/env python3
"""Example smoke tests for Day 22."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from day22 import solve as solve1, min_mana_to_win
from day22_part2 import solve as solve2


def main() -> None:
    # Example: Boss HP 13, Damage 8. Min mana = 212 (four Magic Missiles: 4*53).
    example = "Hit Points: 13\nDamage: 8\n"
    assert min_mana_to_win(13, 8, hard_mode=False) == 212
    assert solve1(example) == 212
    # Part 2 hard mode: lose 1 HP per player turn; answer higher
    ans2 = solve2(example)
    assert ans2 >= 212
    print("Day 22 examples OK")


if __name__ == "__main__":
    main()
