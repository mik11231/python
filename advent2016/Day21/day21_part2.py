#!/usr/bin/env python3
"""Advent of Code 2016 Day 21 Part 2: unscramble target string."""

from itertools import permutations
from pathlib import Path


def rot_left(s: list[str], k: int) -> list[str]:
    """Rotate list left by k."""
    k %= len(s)
    return s[k:] + s[:k]


def rot_right(s: list[str], k: int) -> list[str]:
    """Rotate list right by k."""
    k %= len(s)
    return s[-k:] + s[:-k]


def apply_ops(text: str, start: str) -> str:
    """Apply scrambling operations to start string."""
    arr = list(start)
    for ln in text.splitlines():
        w = ln.split()
        if not w:
            continue
        if w[0] == "swap" and w[1] == "position":
            x, y = int(w[2]), int(w[5])
            arr[x], arr[y] = arr[y], arr[x]
        elif w[0] == "swap" and w[1] == "letter":
            x, y = w[2], w[5]
            arr = [y if ch == x else x if ch == y else ch for ch in arr]
        elif w[0] == "rotate" and w[1] in {"left", "right"}:
            k = int(w[2])
            arr = rot_left(arr, k) if w[1] == "left" else rot_right(arr, k)
        elif w[0] == "rotate" and w[1] == "based":
            x = w[-1]
            i = arr.index(x)
            k = 1 + i + (1 if i >= 4 else 0)
            arr = rot_right(arr, k)
        elif w[0] == "reverse":
            x, y = int(w[2]), int(w[4])
            arr = arr[:x] + list(reversed(arr[x : y + 1])) + arr[y + 1 :]
        elif w[0] == "move":
            x, y = int(w[2]), int(w[5])
            ch = arr.pop(x)
            arr.insert(y, ch)
    return "".join(arr)


def solve(s: str) -> str:
    """Return original password that scrambles to 'fbgdceah'."""
    target = "fbgdceah"
    for p in permutations(target):
        cand = "".join(p)
        if apply_ops(s, cand) == target:
            return cand
    raise ValueError("No preimage found")


if __name__ == "__main__":
    text = Path(__file__).with_name("d21_input.txt").read_text(encoding="utf-8")
    print(solve(text))
