#!/usr/bin/env python3
"""Advent of Code 2016 Day 10 Part 2: multiply outputs 0,1,2."""

from collections import defaultdict, deque
from pathlib import Path
import re


VAL_RE = re.compile(r"value (\d+) goes to bot (\d+)")
RULE_RE = re.compile(
    r"bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)"
)


def simulate(s: str) -> dict[int, list[int]]:
    """Run bot simulation and return outputs bins."""
    bots: dict[int, list[int]] = defaultdict(list)
    rules: dict[int, tuple[tuple[str, int], tuple[str, int]]] = {}
    outputs: dict[int, list[int]] = defaultdict(list)

    for line in s.splitlines():
        line = line.strip()
        if not line:
            continue
        m = VAL_RE.match(line)
        if m:
            v, b = int(m.group(1)), int(m.group(2))
            bots[b].append(v)
            continue
        m = RULE_RE.match(line)
        if m:
            b = int(m.group(1))
            low = (m.group(2), int(m.group(3)))
            high = (m.group(4), int(m.group(5)))
            rules[b] = (low, high)

    q = deque([b for b, vals in bots.items() if len(vals) >= 2])
    while q:
        b = q.popleft()
        if len(bots[b]) < 2 or b not in rules:
            continue
        lo, hi = sorted(bots[b][:2])
        bots[b] = bots[b][2:]
        (lt, li), (ht, hi_id) = rules[b]

        if lt == "bot":
            bots[li].append(lo)
            if len(bots[li]) >= 2:
                q.append(li)
        else:
            outputs[li].append(lo)

        if ht == "bot":
            bots[hi_id].append(hi)
            if len(bots[hi_id]) >= 2:
                q.append(hi_id)
        else:
            outputs[hi_id].append(hi)

    return outputs


def solve(s: str) -> int:
    """Return product of first values in output bins 0, 1, and 2."""
    outputs = simulate(s)
    return outputs[0][0] * outputs[1][0] * outputs[2][0]


if __name__ == "__main__":
    text = Path(__file__).with_name("d10_input.txt").read_text(encoding="utf-8")
    print(solve(text))
