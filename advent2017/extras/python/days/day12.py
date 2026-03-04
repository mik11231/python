#!/usr/bin/env python3
"""AoC 2017 Day 12 fancy Python implementation (graph connectivity analytics)."""

from __future__ import annotations

import argparse
import hashlib
import time
from collections import deque
from pathlib import Path

EXPECTED_SHA256 = "5a807a689f833a1add89ef7c1215b693721849db8347b273bca570346357377c"
EXPECTED_PART1 = "239"
EXPECTED_PART2 = "215"


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
        Path("advent2017/Day12/d12_input.txt"),
        Path("Day12/d12_input.txt"),
        Path("../Day12/d12_input.txt"),
        Path("../../Day12/d12_input.txt"),
        Path(__file__).resolve().parents[2] / "Day12" / "d12_input.txt",
    ]
    for c in cands:
        if c.exists():
            return c.resolve()
    raise FileNotFoundError("input not found for day 12")


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


def parse_graph(raw: str) -> dict[int, list[int]]:
    """
    Run `parse_graph` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: raw.
    - Returns the computed result for this stage of the pipeline.
    """
    g: dict[int, list[int]] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        left, right = line.split("<->")
        u = int(left.strip())
        nbrs = [int(x.strip()) for x in right.split(",")]
        g[u] = nbrs
    return g


def bfs_component(g: dict[int, list[int]], start: int, seen: set[int]) -> set[int]:
    """
    Run `bfs_component` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: g, start, seen.
    - Returns the computed result for this stage of the pipeline.
    """
    q = deque([start])
    comp: set[int] = {start}
    seen.add(start)
    while q:
        u = q.popleft()
        for v in g.get(u, []):
            if v in seen:
                continue
            seen.add(v)
            comp.add(v)
            q.append(v)
    return comp


def solve(raw: str) -> tuple[int, int]:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: raw.
    - Returns the computed result for this stage of the pipeline.
    """
    g = parse_graph(raw)
    seen: set[int] = set()

    group0 = bfs_component(g, 0, seen)
    groups = 1

    for node in g:
        if node in seen:
            continue
        bfs_component(g, node, seen)
        groups += 1

    return len(group0), groups


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
    ap = argparse.ArgumentParser(description="AoC 2017 Day 12 fancy Python")
    ap.add_argument("--part", type=int, required=True, choices=[1, 2])
    ap.add_argument("--input")
    args = ap.parse_args()

    input_path = Path(args.input).resolve() if args.input else default_input_path()
    got_sha = sha256_file(input_path)
    if got_sha != EXPECTED_SHA256:
        raise SystemExit(f"checksum mismatch: {got_sha} != {EXPECTED_SHA256}")

    raw = input_path.read_text(encoding="utf-8")

    t0 = time.perf_counter_ns()
    p1, p2 = solve(raw)
    answer = str(p1 if args.part == 1 else p2)
    runtime_ms = (time.perf_counter_ns() - t0) / 1e6

    expected = EXPECTED_PART1 if args.part == 1 else EXPECTED_PART2
    if answer != expected:
        raise SystemExit(f"answer mismatch for part {args.part}: got {answer!r}, expected {expected!r}")

    print(answer)
    print(f"[python-fancy] day=12 part={args.part} runtime_ms={runtime_ms:.3f}", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
