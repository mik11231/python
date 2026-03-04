#!/usr/bin/env python3
"""Advent of Code 2015 Day 22 — Wizard Simulator 20XX.

Minimum mana to win via DFS with branch-and-bound pruning over game states.
Boss damage from input; apply effects then player then boss.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.parsing import lines, ints


def parse_boss(s: str) -> tuple[int, int]:
    """Return (boss_hp, boss_damage)."""
    boss_hp, boss_damage = 0, 0
    for line in lines(s):
        if "Hit Points" in line:
            boss_hp = ints(line)[0]
        if "Damage" in line:
            boss_damage = ints(line)[0]
    return boss_hp, boss_damage


# Spells: (cost, immediate_damage, immediate_heal, effect_name, effect_turns)
# effect_turns 0 = instant only
SPELLS = [
    (53, 4, 0, None, 0),   # Magic Missile
    (73, 2, 2, None, 0),   # Drain
    (113, 0, 0, "shield", 6),
    (173, 0, 0, "poison", 6),
    (229, 0, 0, "recharge", 5),
]


def apply_effects(
    player_hp: int,
    boss_hp: int,
    mana: int,
    shield: int,
    poison: int,
    recharge: int,
) -> tuple[int, int, int, int, int, int]:
    """Apply start-of-turn effects; return (player_hp, boss_hp, mana, s, p, r)."""
    if poison > 0:
        boss_hp -= 3
    if recharge > 0:
        mana += 101
    shield = max(0, shield - 1)
    poison = max(0, poison - 1)
    recharge = max(0, recharge - 1)
    return player_hp, boss_hp, mana, shield, poison, recharge


def _dfs(
    player_hp: int,
    b_hp: int,
    mana: int,
    shield: int,
    poison: int,
    recharge: int,
    is_player_turn: bool,
    mana_spent: int,
    boss_damage: int,
    hard_mode: bool,
    best: list[int],
) -> None:
    """DFS with prune by best; updates best[0] with minimum mana to win."""
    if mana_spent >= best[0]:
        return
    # Hard mode: lose 1 HP at start of player turn (before other effects)
    if is_player_turn and hard_mode:
        player_hp -= 1
        if player_hp <= 0:
            return
    armor_this_turn = 7 if shield > 0 else 0
    player_hp, b_hp, mana, shield, poison, recharge = apply_effects(
        player_hp, b_hp, mana, shield, poison, recharge
    )
    if b_hp <= 0:
        best[0] = min(best[0], mana_spent)
        return
    if is_player_turn:
        for cost, dmg, heal, effect, turns in SPELLS:
            if mana < cost:
                continue
            if effect == "shield" and shield > 0:
                continue
            if effect == "poison" and poison > 0:
                continue
            if effect == "recharge" and recharge > 0:
                continue
            new_mana = mana - cost
            new_b = b_hp - dmg
            new_p_hp = player_hp + heal
            new_s, new_p, new_r = shield, poison, recharge
            if effect == "shield":
                new_s = turns
            elif effect == "poison":
                new_p = turns
            elif effect == "recharge":
                new_r = turns
            if new_b <= 0:
                best[0] = min(best[0], mana_spent + cost)
                continue
            _dfs(
                new_p_hp, new_b, new_mana, new_s, new_p, new_r,
                False, mana_spent + cost, boss_damage, hard_mode, best,
            )
    else:
        dmg = max(1, boss_damage - armor_this_turn)
        new_p_hp = player_hp - dmg
        if new_p_hp <= 0:
            return
        _dfs(
            new_p_hp, b_hp, mana, shield, poison, recharge,
            True, mana_spent, boss_damage, hard_mode, best,
        )


def min_mana_to_win(
    boss_hp: int,
    boss_damage: int,
    hard_mode: bool = False,
) -> int:
    """DFS with best-cost pruning to find minimum mana to win."""
    best = [10**9]
    _dfs(50, boss_hp, 500, 0, 0, 0, True, 0, boss_damage, hard_mode, best)
    return best[0] if best[0] != 10**9 else -1


def solve(s: str) -> int:
    """Return minimum mana to win (no hard mode)."""
    boss_hp, boss_damage = parse_boss(s)
    return min_mana_to_win(boss_hp, boss_damage, hard_mode=False)


if __name__ == "__main__":
    text = Path(__file__).with_name("d22_input.txt").read_text(encoding="utf-8")
    print(solve(text))
