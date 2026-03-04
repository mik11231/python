#!/usr/bin/env python3
"""Advent of Code 2016 Day 15 Part 1: Timing is Everything."""

from pathlib import Path
import re


PAT = re.compile(
    r"Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+)."
)


def solve(s: str) -> int:
    """Find earliest time t where capsule falls through all discs."""
    discs: list[tuple[int, int, int]] = []
    for ln in s.splitlines():
        m = PAT.match(ln.strip())
        if m:
            discs.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))

    t = 0
    step = 1
    for idx, mod, pos in discs:
        # Need (pos + t + idx) % mod == 0
        while (pos + t + idx) % mod != 0:
            t += step
        step *= mod
    return t


if __name__ == "__main__":
    text = Path(__file__).with_name("d15_input.txt").read_text(encoding="utf-8")
    print(solve(text))
