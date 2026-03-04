#!/usr/bin/env python3
"""AoC 2017 Day 3 fancy Python implementation (real algorithms for both parts)."""

from __future__ import annotations

import argparse
import hashlib
import time
from pathlib import Path

EXPECTED_SHA256 = "697301449f3f32ff9e73436c0ee11191f61f63d01afda5637bf644c5aa6042bc"
EXPECTED_PART1 = "371"
EXPECTED_PART2 = "369601"
NEI = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]


def default_input_path() -> Path:
    """
    Run `default_input_path` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Returns the computed result for this stage of the pipeline.
    """
    cands = [
        Path("advent2017/Day3/d3_input.txt"),
        Path("Day3/d3_input.txt"),
        Path("../Day3/d3_input.txt"),
        Path("../../Day3/d3_input.txt"),
        Path(__file__).resolve().parents[2] / "Day3" / "d3_input.txt",
    ]
    for c in cands:
        if c.exists():
            return c.resolve()
    raise FileNotFoundError("input not found for day 3")


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


def parse_target(raw: str) -> int:
    """
    Run `parse_target` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: raw.
    - Returns the computed result for this stage of the pipeline.
    """
    return int(raw.strip())


def solve_part1(n: int) -> int:
    """
    Run `solve_part1` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: n.
    - Returns the computed result for this stage of the pipeline.
    """
    if n == 1:
        return 0
    layer = 0
    while (2 * layer + 1) ** 2 < n:
        layer += 1
    side = 2 * layer
    maxv = (2 * layer + 1) ** 2
    mids = [maxv - layer - side * i for i in range(4)]
    return layer + min(abs(n - m) for m in mids)


def solve_part2(target: int) -> int:
    """
    Run `solve_part2` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: target.
    - Returns the computed result for this stage of the pipeline.
    """
    grid: dict[tuple[int, int], int] = {(0, 0): 1}
    x = y = 0
    step = 1

    def write_and_check(nx: int, ny: int) -> int:
        """
        Run `write_and_check` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: nx, ny.
        - Returns the computed result for this stage of the pipeline.
        """
        value = sum(grid.get((nx + dx, ny + dy), 0) for dx, dy in NEI)
        if value > target:
            return value
        grid[(nx, ny)] = value
        return 0

    while True:
        for _ in range(step):
            x += 1
            out = write_and_check(x, y)
            if out:
                return out
        for _ in range(step):
            y += 1
            out = write_and_check(x, y)
            if out:
                return out
        step += 1
        for _ in range(step):
            x -= 1
            out = write_and_check(x, y)
            if out:
                return out
        for _ in range(step):
            y -= 1
            out = write_and_check(x, y)
            if out:
                return out
        step += 1


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
    ap = argparse.ArgumentParser(description="AoC 2017 Day 3 fancy Python")
    ap.add_argument("--part", type=int, required=True, choices=[1, 2])
    ap.add_argument("--input")
    args = ap.parse_args()

    input_path = Path(args.input).resolve() if args.input else default_input_path()
    got_sha = sha256_file(input_path)
    if got_sha != EXPECTED_SHA256:
        raise SystemExit(f"checksum mismatch: {got_sha} != {EXPECTED_SHA256}")

    target = parse_target(input_path.read_text(encoding="utf-8"))

    t0 = time.perf_counter_ns()
    if args.part == 1:
        answer = str(solve_part1(target))
        expected = EXPECTED_PART1
    else:
        answer = str(solve_part2(target))
        expected = EXPECTED_PART2
    runtime_ms = (time.perf_counter_ns() - t0) / 1e6

    if answer != expected:
        raise SystemExit(f"answer mismatch for part {args.part}: got {answer!r}, expected {expected!r}")

    print(answer)
    print(f"[python-fancy] day=3 part={args.part} runtime_ms={runtime_ms:.3f}", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
