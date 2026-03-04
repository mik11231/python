#!/usr/bin/env python3
"""Shared knot-hash helpers for Advent of Code 2017."""


def sparse_round(a: list[int], lengths: list[int], pos: int, skip: int) -> tuple[int, int]:
    """
    Run `sparse_round` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: a, lengths, pos, skip.
    - Returns the computed result for this stage of the pipeline.
    """
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
    """
    Run `knot_hash` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: text.
    - Returns the computed result for this stage of the pipeline.
    """
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
