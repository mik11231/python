#!/usr/bin/env python3
"""
advent2017/extras/python/days/day25.py

Implementation Notes:
- This module is intentionally documented in depth so the solution can be
  reconstructed from comments/docstrings after long periods away from the code.
- The code follows a parse -> transform -> solve pipeline where applicable.
- Year scope: advent2017.
- Complexity and data-structure tradeoffs are described in function docstrings below.
"""

from __future__ import annotations

import argparse
import hashlib
import time
from pathlib import Path

EXPECTED_SHA = "6419303e9eeb435a39b6e7d17236cb0d3fdfc9b0c2e5d5da8a9864b527c7e873"
EXPECTED_PART1 = "3145"
EXPECTED_PART2 = "Merry Christmas"


def resolve_input(provided: str | None) -> Path:
    """
    Run `resolve_input` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: provided.
    - Returns the computed result for this stage of the pipeline.
    """
    if provided:
        return Path(provided).resolve()
    for c in (
        "advent2017/Day25/d25_input.txt",
        "Day25/d25_input.txt",
        "../Day25/d25_input.txt",
        "../../Day25/d25_input.txt",
    ):
        p = Path(c)
        if p.exists():
            return p.resolve()
    raise SystemExit("input not found")


def sha256_file(path: Path) -> str:
    """
    Run `sha256_file` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: path.
    - Returns the computed result for this stage of the pipeline.
    """
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_tm(text: str) -> tuple[int, int, list[list[tuple[int, int, int]]]]:
    """
    Run `parse_tm` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: text.
    - Returns the computed result for this stage of the pipeline.
    """
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    start = ord(lines[0][len("Begin in state ")]) - ord("A")
    steps = int(lines[1].split()[5])
    trans: list[list[tuple[int, int, int]]] = [[(0, 0, 0), (0, 0, 0)] for _ in range(26)]
    i = 2
    while i < len(lines):
        st = ord(lines[i][len("In state ")]) - ord("A")
        w0 = int(lines[i + 2][len("- Write the value ")])
        m0 = 1 if lines[i + 3][len("- Move one slot to the ")] == "r" else -1
        n0 = ord(lines[i + 4][len("- Continue with state ")]) - ord("A")
        w1 = int(lines[i + 6][len("- Write the value ")])
        m1 = 1 if lines[i + 7][len("- Move one slot to the ")] == "r" else -1
        n1 = ord(lines[i + 8][len("- Continue with state ")]) - ord("A")
        trans[st][0] = (w0, m0, n0)
        trans[st][1] = (w1, m1, n1)
        i += 9
    return start, steps, trans


def part1(text: str) -> int:
    """
    Run `part1` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: text.
    - Returns the computed result for this stage of the pipeline.
    """
    state, steps, trans = parse_tm(text)
    tape: set[int] = set()
    cur = 0
    for _ in range(steps):
        v = 1 if cur in tape else 0
        w, d, ns = trans[state][v]
        if w:
            tape.add(cur)
        else:
            tape.discard(cur)
        cur += d
        state = ns
    return len(tape)


def main() -> int:
    """
    Run `main` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Returns the computed result for this stage of the pipeline.
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", type=int, choices=[1, 2], required=True)
    ap.add_argument("--input")
    args = ap.parse_args()

    in_path = resolve_input(args.input)
    if sha256_file(in_path) != EXPECTED_SHA:
        raise SystemExit("checksum mismatch")
    text = in_path.read_text(encoding="utf-8")

    t0 = time.perf_counter_ns()
    ans = str(part1(text) if args.part == 1 else EXPECTED_PART2)
    ms = (time.perf_counter_ns() - t0) / 1e6

    expected = EXPECTED_PART1 if args.part == 1 else EXPECTED_PART2
    if ans != expected:
        raise SystemExit(f"answer mismatch: got {ans}, expected {expected}")
    print(ans)
    print(f"[python-fancy] day=25 part={args.part} runtime_ms={ms:.3f}", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
