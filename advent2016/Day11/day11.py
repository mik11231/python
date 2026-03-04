#!/usr/bin/env python3
"""Advent of Code 2016 Day 11 Part 1: Radioisotope Thermoelectric Generators."""

from collections import deque
from pathlib import Path
import re


ITEM_RE = re.compile(r"(\w+)(?:-compatible)? (microchip|generator)")


def parse(s: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    """Parse input into canonical state: elevator floor and sorted (g,m) floors."""
    idx: dict[str, int] = {}
    pairs: list[list[int]] = []
    for f, line in enumerate(s.splitlines()):
        for el, kind in ITEM_RE.findall(line):
            if el not in idx:
                idx[el] = len(pairs)
                pairs.append([-1, -1])
            i = idx[el]
            if kind == "generator":
                pairs[i][0] = f
            else:
                pairs[i][1] = f
    canon = tuple(sorted((g, m) for g, m in pairs))
    return 0, canon


def is_safe(pairs: tuple[tuple[int, int], ...]) -> bool:
    """Check floor safety: chips cannot be with foreign generators."""
    gens_on = [set() for _ in range(4)]
    chips_on = [set() for _ in range(4)]
    for i, (g, m) in enumerate(pairs):
        gens_on[g].add(i)
        chips_on[m].add(i)
    for f in range(4):
        if not gens_on[f]:
            continue
        for chip in chips_on[f]:
            if chip not in gens_on[f]:
                return False
    return True


def neigh(e: int, pairs: tuple[tuple[int, int], ...]):
    """Generate reachable next states."""
    items: list[tuple[int, int]] = []  # (pair_index, 0 gen /1 chip)
    for i, (g, m) in enumerate(pairs):
        if g == e:
            items.append((i, 0))
        if m == e:
            items.append((i, 1))

    moves = []
    for i in range(len(items)):
        moves.append([items[i]])
        for j in range(i + 1, len(items)):
            moves.append([items[i], items[j]])

    for d in (1, -1):
        ne = e + d
        if not (0 <= ne < 4):
            continue
        # Prune pointless downward moves when no item below.
        if d == -1:
            if all(g >= e and m >= e for g, m in pairs):
                continue
        for mv in moves:
            arr = [list(x) for x in pairs]
            for pi, kind in mv:
                arr[pi][kind] = ne
            npairs = tuple(sorted((g, m) for g, m in arr))
            if is_safe(npairs):
                yield ne, npairs


def shortest(start: tuple[int, tuple[tuple[int, int], ...]]) -> int:
    """Return minimum elevator moves to bring all items to top floor."""
    goal_pairs = tuple((3, 3) for _ in start[1])
    q = deque([(start[0], start[1], 0)])
    seen = {(start[0], start[1])}
    while q:
        e, pairs, d = q.popleft()
        if pairs == goal_pairs:
            return d
        for ne, np in neigh(e, pairs):
            st = (ne, np)
            if st not in seen:
                seen.add(st)
                q.append((ne, np, d + 1))
    raise ValueError("No solution")


def solve(s: str) -> int:
    """Return shortest move count for part 1."""
    return shortest(parse(s))


if __name__ == "__main__":
    text = Path(__file__).with_name("d11_input.txt").read_text(encoding="utf-8")
    print(solve(text))
