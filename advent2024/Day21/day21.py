#!/usr/bin/env python3
"""Advent of Code 2024 Day 21 Part 1 - Keypad Conundrum.

Chain of 2 intermediate directional-keypad robots plus human controlling a
numeric keypad. Use memoized recursion: cost(a, b, depth) gives the minimum
human keypresses to move a dpad arm from button a to b and press it, expanding
through `depth` layers of directional keypads.
"""
from pathlib import Path
from functools import lru_cache


NUMPAD = {
    '7': (0, 0), '8': (0, 1), '9': (0, 2),
    '4': (1, 0), '5': (1, 1), '6': (1, 2),
    '1': (2, 0), '2': (2, 1), '3': (2, 2),
                  '0': (3, 1), 'A': (3, 2),
}
NUM_GAP = (3, 0)

DPAD = {
                  '^': (0, 1), 'A': (0, 2),
    '<': (1, 0), 'v': (1, 1), '>': (1, 2),
}
DPAD_GAP = (0, 0)


def _build_paths(positions, gap):
    paths = {}
    for a, (r1, c1) in positions.items():
        for b, (r2, c2) in positions.items():
            if a == b:
                paths[(a, b)] = ['']
                continue
            dr, dc = r2 - r1, c2 - c1
            v = ('v' * dr if dr > 0 else '^' * -dr)
            h = ('>' * dc if dc > 0 else '<' * -dc)
            cands = set()
            if (r1, c2) != gap:
                cands.add(h + v)
            if (r2, c1) != gap:
                cands.add(v + h)
            paths[(a, b)] = list(cands)
    return paths


NUM_PATHS = _build_paths(NUMPAD, NUM_GAP)
DPAD_PATHS = _build_paths(DPAD, DPAD_GAP)


@lru_cache(maxsize=None)
def _dpad_cost(a, b, depth):
    if depth == 0:
        return 1
    best = float('inf')
    for path in DPAD_PATHS[(a, b)]:
        seq = path + 'A'
        cost = prev = 0
        p = 'A'
        for ch in seq:
            cost += _dpad_cost(p, ch, depth - 1)
            p = ch
        best = min(best, cost)
    return best


def solve(s: str, num_robots: int = 2) -> int:
    codes = s.strip().splitlines()
    total = 0
    for code in codes:
        length = 0
        prev = 'A'
        for ch in code:
            best = float('inf')
            for path in NUM_PATHS[(prev, ch)]:
                seq = path + 'A'
                cost, p = 0, 'A'
                for c in seq:
                    cost += _dpad_cost(p, c, num_robots)
                    p = c
                best = min(best, cost)
            length += best
            prev = ch
        total += length * int(code[:-1])
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d21_input.txt").read_text()))
