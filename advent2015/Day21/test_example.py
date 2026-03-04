#!/usr/bin/env python3
"""Example smoke tests for Day 21."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from day21 import parse, player_wins, solve as solve1
from day21_part2 import solve as solve2


def main() -> None:
    # Example: 8 HP, 5 dmg, 5 armor vs 12 HP, 7 dmg, 2 armor -> player wins
    """
    Run `main` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Returns the computed result for this stage of the pipeline.
    """
    assert player_wins(5, 5, 12, 7, 2) is True
    inp = "Hit Points: 12\nDamage: 7\nArmor: 2\n"
    hp, dmg, arm = parse(inp)
    assert hp == 12 and dmg == 7 and arm == 2
    print("Day 21 examples OK")


if __name__ == "__main__":
    main()
