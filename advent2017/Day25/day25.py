#!/usr/bin/env python3
"""Advent of Code 2017 Day 25 Part 1."""

from pathlib import Path
import re


ST_RE = re.compile(r"Begin in state ([A-Z]).")
STEP_RE = re.compile(r"Perform a diagnostic checksum after (\d+) steps.")
STATE_RE = re.compile(r"In state ([A-Z]):")
IF_RE = re.compile(r"If the current value is ([01]):")
WRITE_RE = re.compile(r"- Write the value ([01]).")
MOVE_RE = re.compile(r"- Move one slot to the (left|right).")
NEXT_RE = re.compile(r"- Continue with state ([A-Z]).")


def solve(s: str) -> int:
    lines = [ln.strip() for ln in s.splitlines() if ln.strip()]
    st = ST_RE.match(lines[0]).group(1)
    steps = int(STEP_RE.match(lines[1]).group(1))
    i = 2
    trans = {}
    while i < len(lines):
        m = STATE_RE.match(lines[i])
        if not m:
            i += 1
            continue
        state = m.group(1)
        i += 1
        for _ in range(2):
            cur = int(IF_RE.match(lines[i]).group(1)); i += 1
            w = int(WRITE_RE.match(lines[i]).group(1)); i += 1
            mv = -1 if MOVE_RE.match(lines[i]).group(1) == "left" else 1; i += 1
            ns = NEXT_RE.match(lines[i]).group(1); i += 1
            trans[(state, cur)] = (w, mv, ns)

    tape = set()
    pos = 0
    state = st
    for _ in range(steps):
        cur = 1 if pos in tape else 0
        w, mv, ns = trans[(state, cur)]
        if w == 1:
            tape.add(pos)
        else:
            tape.discard(pos)
        pos += mv
        state = ns
    return len(tape)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d25_input.txt").read_text(encoding="utf-8")))
