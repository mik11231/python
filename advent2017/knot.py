#!/usr/bin/env python3
"""Shared knot-hash helpers for Advent of Code 2017."""


def sparse_round(a: list[int], lengths: list[int], pos: int, skip: int) -> tuple[int, int]:
    n = len(a)
    for ln in lengths:
        for i in range(ln // 2):
            x = (pos + i) % n
            y = (pos + ln - 1 - i) % n
            a[x], a[y] = a[y], a[x]
        pos = (pos + ln + skip) % n
        skip += 1
    return pos, skip


def knot_hash(text: str) -> str:
    a = list(range(256))
    lengths = [ord(c) for c in text] + [17, 31, 73, 47, 23]
    pos = skip = 0
    for _ in range(64):
        pos, skip = sparse_round(a, lengths, pos, skip)
    dense = []
    for b in range(0, 256, 16):
        x = 0
        for v in a[b : b + 16]:
            x ^= v
        dense.append(x)
    return "".join(f"{x:02x}" for x in dense)
