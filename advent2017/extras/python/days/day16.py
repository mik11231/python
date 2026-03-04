#!/usr/bin/env python3
"""AoC 2017 Day 16 fancy Python implementation (dance VM + cycle detection)."""

from __future__ import annotations

import argparse
import hashlib
import time
from pathlib import Path

EXPECTED_SHA256 = "6bb64ef97ccf665f21eccff0a7045717f0a03d39ae06aaac5495dd6fff650818"
EXPECTED_PART1 = "kgdchlfniambejop"
EXPECTED_PART2 = "fjpmholcibdgeakn"


def default_input_path() -> Path:
    cands = [
        Path("advent2017/Day16/d16_input.txt"),
        Path("Day16/d16_input.txt"),
        Path("../Day16/d16_input.txt"),
        Path("../../Day16/d16_input.txt"),
        Path(__file__).resolve().parents[2] / "Day16" / "d16_input.txt",
    ]
    for c in cands:
        if c.exists():
            return c.resolve()
    raise FileNotFoundError("input not found for day 16")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_moves(raw: str) -> list[str]:
    return [m.strip() for m in raw.strip().split(",") if m.strip()]


def apply_once(state: list[str], moves: list[str]) -> None:
    for mv in moves:
        t = mv[0]
        arg = mv[1:]
        if t == "s":
            x = int(arg)
            state[:] = state[-x:] + state[:-x]
        elif t == "x":
            a, b = map(int, arg.split("/"))
            state[a], state[b] = state[b], state[a]
        elif t == "p":
            a, b = arg.split("/")
            ia = state.index(a)
            ib = state.index(b)
            state[ia], state[ib] = state[ib], state[ia]
        else:
            raise ValueError("bad move")


def dance(moves: list[str], rounds: int) -> str:
    state = list("abcdefghijklmnop")
    seen: dict[str, int] = {}

    i = 0
    while i < rounds:
        key = "".join(state)
        if key in seen:
            cycle = i - seen[key]
            rem = (rounds - i) % cycle
            for _ in range(rem):
                apply_once(state, moves)
            return "".join(state)
        seen[key] = i
        apply_once(state, moves)
        i += 1

    return "".join(state)


def main() -> int:
    ap = argparse.ArgumentParser(description="AoC 2017 Day 16 fancy Python")
    ap.add_argument("--part", type=int, required=True, choices=[1, 2])
    ap.add_argument("--input")
    args = ap.parse_args()

    input_path = Path(args.input).resolve() if args.input else default_input_path()
    got_sha = sha256_file(input_path)
    if got_sha != EXPECTED_SHA256:
        raise SystemExit(f"checksum mismatch: {got_sha} != {EXPECTED_SHA256}")

    moves = parse_moves(input_path.read_text(encoding="utf-8"))

    t0 = time.perf_counter_ns()
    answer = dance(moves, 1 if args.part == 1 else 1_000_000_000)
    runtime_ms = (time.perf_counter_ns() - t0) / 1e6

    expected = EXPECTED_PART1 if args.part == 1 else EXPECTED_PART2
    if answer != expected:
        raise SystemExit(f"answer mismatch for part {args.part}: got {answer!r}, expected {expected!r}")

    print(answer)
    print(f"[python-fancy] day=16 part={args.part} runtime_ms={runtime_ms:.3f}", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
