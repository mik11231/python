#!/usr/bin/env python3
"""Advent of Code 2015 Day 21 Part 2 — Maximum gold to lose."""
from pathlib import Path
import re

from day21 import parse, player_wins, WEAPONS, ARMOR, RINGS


def loadouts() -> list[tuple[int, int, int]]:
    """Yield (cost, damage, armor) for each valid loadout."""
    for w in WEAPONS:
        for a in ARMOR:
            cost = w[0] + a[0]
            dmg = w[1] + a[1]
            arm = w[2] + a[2]
            yield cost, dmg, arm
            for r in RINGS[1:]:
                yield cost + r[0], dmg + r[1], arm + r[2]
            for i, r1 in enumerate(RINGS[1:]):
                for r2 in RINGS[1:][i + 1:]:
                    yield cost + r1[0] + r2[0], dmg + r1[1] + r2[1], arm + r1[2] + r2[2]


def solve(s: str) -> int:
    """Return maximum gold spent and still lose."""
    boss_hp, boss_damage, boss_armor = parse(s)
    best = 0
    for cost, dmg, arm in loadouts():
        if not player_wins(dmg, arm, boss_hp, boss_damage, boss_armor):
            if cost > best:
                best = cost
    return best


if __name__ == "__main__":
    text = Path(__file__).with_name("d21_input.txt").read_text(encoding="utf-8")
    print(solve(text))
