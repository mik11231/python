#!/usr/bin/env python3
"""Advent of Code 2015 Day 21 — RPG Simulator.

Boss stats and shop. Turn-based: player hits first. Part 1: minimum gold to win.
"""
from pathlib import Path
import re

# Shop: (cost, damage, armor)
WEAPONS = [
    (8, 4, 0),
    (10, 5, 0),
    (25, 6, 0),
    (40, 7, 0),
    (74, 8, 0),
]
ARMOR = [
    (0, 0, 0),   # none
    (13, 0, 1),
    (31, 0, 2),
    (53, 0, 3),
    (75, 0, 4),
    (102, 0, 5),
]
RINGS = [
    (0, 0, 0),   # none
    (25, 1, 0),
    (50, 2, 0),
    (100, 3, 0),
    (20, 0, 1),
    (40, 0, 2),
    (80, 0, 3),
]


def parse(s: str) -> tuple[int, int, int]:
    """Return (boss_hp, boss_damage, boss_armor)."""
    lines = [line.strip() for line in s.strip().splitlines() if line.strip()]
    hp = damage = armor = 0
    for line in lines:
        if "Hit Points" in line:
            hp = int(re.search(r"\d+", line).group())
        elif "Damage" in line:
            damage = int(re.search(r"\d+", line).group())
        elif "Armor" in line:
            armor = int(re.search(r"\d+", line).group())
    return hp, damage, armor


def loadouts() -> list[tuple[int, int, int, int]]:
    """Yield (cost, damage, armor) for each valid loadout."""
    for w in WEAPONS:
        for a in ARMOR:
            for r in [None]:  # 0 rings
                cost = w[0] + a[0]
                dmg = w[1] + a[1]
                arm = w[2] + a[2]
                yield cost, dmg, arm
            for r in RINGS[1:]:  # 1 ring
                cost = w[0] + a[0] + r[0]
                dmg = w[1] + a[1] + r[1]
                arm = w[2] + a[2] + r[2]
                yield cost, dmg, arm
            for i, r1 in enumerate(RINGS[1:]):
                for r2 in RINGS[1:][i + 1:]:  # 2 different rings
                    cost = w[0] + a[0] + r1[0] + r2[0]
                    dmg = w[1] + a[1] + r1[1] + r2[1]
                    arm = w[2] + a[2] + r1[2] + r2[2]
                    yield cost, dmg, arm


def player_wins(player_damage: int, player_armor: int, boss_hp: int, boss_damage: int, boss_armor: int) -> bool:
    """Simulate fight: player goes first, 100 HP. Return True if player wins."""
    php, bhp = 100, boss_hp
    while True:
        bhp -= max(1, player_damage - boss_armor)
        if bhp <= 0:
            return True
        php -= max(1, boss_damage - player_armor)
        if php <= 0:
            return False


def solve(s: str) -> int:
    """Return minimum gold to win."""
    boss_hp, boss_damage, boss_armor = parse(s)
    best = None
    for cost, dmg, arm in loadouts():
        if player_wins(dmg, arm, boss_hp, boss_damage, boss_armor):
            if best is None or cost < best:
                best = cost
    return best or 0


if __name__ == "__main__":
    text = Path(__file__).with_name("d21_input.txt").read_text(encoding="utf-8")
    print(solve(text))
