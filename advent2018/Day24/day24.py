"""Advent of Code 2018 solution module."""

import re
from dataclasses import dataclass
from pathlib import Path


LINE_RE = re.compile(
    r"(\d+) units each with (\d+) hit points(?: \(([^)]*)\))? with an attack that does "
    r"(\d+) (\w+) damage at initiative (\d+)"
)


@dataclass
class Group:
    army: str
    id: int
    units: int
    hp: int
    attack: int
    attack_type: str
    initiative: int
    weak: set[str]
    immune: set[str]

    @property
    def power(self) -> int:
        """
        Run `power` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: self.
        - Returns the computed result for this stage of the pipeline.
        """
        return self.units * self.attack


def parse_modifiers(text: str | None):
    """
    Run `parse_modifiers` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: text.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    weak = set()
    immune = set()
    if not text:
        return weak, immune
    for part in text.split('; '):
        if part.startswith('weak to '):
            weak.update(x.strip() for x in part[len('weak to '):].split(','))
        elif part.startswith('immune to '):
            immune.update(x.strip() for x in part[len('immune to '):].split(','))
    return weak, immune


def load(path: Path):
    """
    Run `load` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: path.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    groups = []
    army = None
    gid = {'Immune System': 0, 'Infection': 0}

    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        if line.endswith(':'):
            army = line[:-1]
            continue

        m = LINE_RE.fullmatch(line)
        units, hp, mods, attack, attack_type, init = m.groups()
        weak, immune = parse_modifiers(mods)
        gid[army] += 1
        groups.append(
            Group(
                army=army,
                id=gid[army],
                units=int(units),
                hp=int(hp),
                attack=int(attack),
                attack_type=attack_type,
                initiative=int(init),
                weak=weak,
                immune=immune,
            )
        )
    return groups


def damage(attacker: Group, defender: Group) -> int:
    """
    Run `damage` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: attacker, defender.
    - Returns the computed result for this stage of the pipeline.
    """
    if attacker.attack_type in defender.immune:
        return 0
    d = attacker.power
    if attacker.attack_type in defender.weak:
        d *= 2
    return d


def fight(initial_groups: list[Group], boost: int = 0):
    """Simulate battle. Return (winner_army or None on stalemate, remaining_units)."""
    groups = []
    for g in initial_groups:
        ng = Group(**g.__dict__)
        if ng.army == 'Immune System':
            ng.attack += boost
        groups.append(ng)

    while True:
        groups = [g for g in groups if g.units > 0]
        armies = {g.army for g in groups}
        if len(armies) == 1:
            winner = next(iter(armies))
            return winner, sum(g.units for g in groups)

        # Target selection: descending power, then initiative.
        order = sorted(groups, key=lambda g: (g.power, g.initiative), reverse=True)
        chosen = set()
        targets = {}

        for a in order:
            enemies = [
                e
                for e in groups
                if e.army != a.army
                and (e.army, e.id) not in chosen
                and e.units > 0
                and damage(a, e) > 0
            ]
            if not enemies:
                continue
            enemies.sort(key=lambda e: (damage(a, e), e.power, e.initiative), reverse=True)
            t = enemies[0]
            targets[(a.army, a.id)] = t
            chosen.add((t.army, t.id))

        # Attack phase: descending initiative.
        attack_order = sorted(groups, key=lambda g: g.initiative, reverse=True)
        killed_any = False

        for a in attack_order:
            key = (a.army, a.id)
            if a.units <= 0 or key not in targets:
                continue
            t = targets[key]
            if t.units <= 0:
                continue
            d = damage(a, t)
            killed = min(t.units, d // t.hp)
            if killed > 0:
                killed_any = True
            t.units -= killed

        if not killed_any:
            return None, sum(g.units for g in groups)


def solve(groups: list[Group]) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: groups.
    - Returns the computed result for this stage of the pipeline.
    """
    _, units = fight(groups, boost=0)
    return units


if __name__ == '__main__':
    print(solve(load(Path(__file__).with_name('d24_input.txt'))))
