#!/usr/bin/env python3
"""Advent of Code 2015 Day 11 — Corporate Policy.

Password: increment (a->b, z->a, skip i,l,o); must have 2+ non-overlapping pairs
and one run of 3 consecutive letters. Return next valid password.
"""
from pathlib import Path


def inc_char(c: str) -> tuple[str, bool]:
    """Return (next char, carry). Skip i, l, o."""
    n = ord(c) + 1
    while n <= ord("z"):
        if chr(n) not in "ilo":
            return chr(n), False
        n += 1
    return "a", True


def increment(s: str) -> str:
    """Increment password from right; skip i, l, o."""
    chars = list(s)
    i = len(chars) - 1
    while i >= 0:
        next_c, carry = inc_char(chars[i])
        chars[i] = next_c
        if not carry:
            break
        i -= 1
    return "".join(chars)


def has_run_of_three(s: str) -> bool:
    """True if s contains abc, bcd, ... xyz."""
    for i in range(len(s) - 2):
        a, b, c = ord(s[i]), ord(s[i + 1]), ord(s[i + 2])
        if b == a + 1 and c == b + 1:
            return True
    return False


def has_two_pairs(s: str) -> bool:
    """True if s has at least 2 non-overlapping pairs (aa, bb, ...)."""
    pairs: set[str] = set()
    i = 0
    while i < len(s) - 1:
        if s[i] == s[i + 1]:
            pairs.add(s[i])
            i += 2
        else:
            i += 1
    return len(pairs) >= 2


def is_valid(s: str) -> bool:
    if "i" in s or "l" in s or "o" in s:
        return False
    return has_run_of_three(s) and has_two_pairs(s)


def next_valid(s: str) -> str:
    """Return next valid password after s (may equal s if already valid)."""
    s = s.strip()
    while True:
        s = increment(s)
        if is_valid(s):
            return s


def solve(s: str) -> str:
    """Return next valid password after input."""
    return next_valid(s)


if __name__ == "__main__":
    text = Path(__file__).with_name("d11_input.txt").read_text(encoding="utf-8")
    print(solve(text))
