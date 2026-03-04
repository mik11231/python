#!/usr/bin/env python3
"""Advent of Code 2015 Day 22 Part 2 — Wizard Simulator (hard mode).

Lose 1 HP at the start of each player turn. Minimum mana to win.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.parsing import lines, ints

# Reuse min_mana_to_win from day22
from day22 import parse_boss, min_mana_to_win


def solve(s: str) -> int:
    """Return minimum mana to win in hard mode (lose 1 HP per player turn)."""
    boss_hp, boss_damage = parse_boss(s)
    return min_mana_to_win(boss_hp, boss_damage, hard_mode=True)


if __name__ == "__main__":
    text = Path(__file__).with_name("d22_input.txt").read_text(encoding="utf-8")
    print(solve(text))
