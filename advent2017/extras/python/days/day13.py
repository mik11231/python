#!/usr/bin/env python3
"""AoC 2017 Day 13 fancy Python implementation (scanner periodic analysis)."""

from __future__ import annotations

import argparse
import hashlib
import time
from pathlib import Path

EXPECTED_SHA256 = "b59ed1486b6ec731cb7c2f55fdfec971d1157b9411fb823f9ddf0a3839d12cc8"
EXPECTED_PART1 = "2604"
EXPECTED_PART2 = "3941460"


def default_input_path() -> Path:
    cands = [
        Path("advent2017/Day13/d13_input.txt"),
        Path("Day13/d13_input.txt"),
        Path("../Day13/d13_input.txt"),
        Path("../../Day13/d13_input.txt"),
        Path(__file__).resolve().parents[2] / "Day13" / "d13_input.txt",
    ]
    for c in cands:
        if c.exists():
            return c.resolve()
    raise FileNotFoundError("input not found for day 13")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_layers(raw: str) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    # part1 uses (depth, range); part2 uses (bad_delay_mod_period, period)
    p1: list[tuple[int, int]] = []
    p2: list[tuple[int, int]] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        d_s, r_s = line.split(":")
        depth = int(d_s.strip())
        rng = int(r_s.strip())
        period = 2 * (rng - 1)
        p1.append((depth, rng))
        p2.append(((-depth) % period, period))
    # Highest-frequency failures first for early exit in search loop.
    p2.sort(key=lambda x: x[1])
    return p1, p2


def solve_part1(layers: list[tuple[int, int]]) -> int:
    severity = 0
    for depth, rng in layers:
        if depth % (2 * (rng - 1)) == 0:
            severity += depth * rng
    return severity


def solve_part2(layers: list[tuple[int, int]]) -> int:
    layers_loc = layers
    delay = 0
    while True:
        for bad, period in layers_loc:
            if delay % period == bad:
                break
        else:
            return delay
        delay += 1


def main() -> int:
    ap = argparse.ArgumentParser(description="AoC 2017 Day 13 fancy Python")
    ap.add_argument("--part", type=int, required=True, choices=[1, 2])
    ap.add_argument("--input")
    args = ap.parse_args()

    input_path = Path(args.input).resolve() if args.input else default_input_path()
    got_sha = sha256_file(input_path)
    if got_sha != EXPECTED_SHA256:
        raise SystemExit(f"checksum mismatch: {got_sha} != {EXPECTED_SHA256}")

    layers_p1, layers_p2 = parse_layers(input_path.read_text(encoding="utf-8"))

    t0 = time.perf_counter_ns()
    answer = str(solve_part1(layers_p1) if args.part == 1 else solve_part2(layers_p2))
    runtime_ms = (time.perf_counter_ns() - t0) / 1e6

    expected = EXPECTED_PART1 if args.part == 1 else EXPECTED_PART2
    if answer != expected:
        raise SystemExit(f"answer mismatch for part {args.part}: got {answer!r}, expected {expected!r}")

    print(answer)
    print(f"[python-fancy] day=13 part={args.part} runtime_ms={runtime_ms:.3f}", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
