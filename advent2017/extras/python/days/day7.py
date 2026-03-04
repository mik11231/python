#!/usr/bin/env python3
"""AoC 2017 Day 7 fancy Python implementation (real algorithms for both parts)."""

from __future__ import annotations

import argparse
import hashlib
import time
from collections import Counter
from functools import lru_cache
from pathlib import Path

EXPECTED_SHA256 = "3fd999ac97824b5f8cd2bcbf5c69704a352a0a4bbf9735b0fcc289932fcaeac6"
EXPECTED_PART1 = "mwzaxaj"
EXPECTED_PART2 = "1219"


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
        Path("advent2017/Day7/d7_input.txt"),
        Path("Day7/d7_input.txt"),
        Path("../Day7/d7_input.txt"),
        Path("../../Day7/d7_input.txt"),
        Path(__file__).resolve().parents[2] / "Day7" / "d7_input.txt",
    ]
    for c in cands:
        if c.exists():
            return c.resolve()
    raise FileNotFoundError("input not found for day 7")


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


def parse_tower(raw: str) -> tuple[dict[str, int], dict[str, list[str]], dict[str, str]]:
    """
    Run `parse_tower` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: raw.
    - Returns the computed result for this stage of the pipeline.
    """
    weights: dict[str, int] = {}
    children: dict[str, list[str]] = {}
    parent: dict[str, str] = {}

    for line in raw.splitlines():
        if not line.strip():
            continue
        left, *right = line.split("->")
        toks = left.split()
        name = toks[0]
        weight = int(toks[1][1:-1])
        weights[name] = weight

        kids: list[str] = []
        if right:
            kids = [x.strip() for x in right[0].split(",")]
            for c in kids:
                parent[c] = name
        children[name] = kids

    return weights, children, parent


def find_root(weights: dict[str, int], parent: dict[str, str]) -> str:
    """
    Run `find_root` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: weights, parent.
    - Returns the computed result for this stage of the pipeline.
    """
    return next(n for n in weights if n not in parent)


def solve_part1(raw: str) -> str:
    """
    Run `solve_part1` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: raw.
    - Returns the computed result for this stage of the pipeline.
    """
    weights, _, parent = parse_tower(raw)
    return find_root(weights, parent)


def solve_part2(raw: str) -> int:
    """
    Run `solve_part2` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: raw.
    - Returns the computed result for this stage of the pipeline.
    """
    weights, children, parent = parse_tower(raw)
    root = find_root(weights, parent)

    @lru_cache(maxsize=None)
    def total(node: str) -> int:
        """
        Run `total` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: node.
        - Returns the computed result for this stage of the pipeline.
        """
        return weights[node] + sum(total(c) for c in children[node])

    def dfs(node: str) -> int | None:
        """
        Run `dfs` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: node.
        - Returns the computed result for this stage of the pipeline.
        """
        if not children[node]:
            return None

        ts = [total(c) for c in children[node]]
        if len(set(ts)) <= 1:
            return None

        cnt = Counter(ts)
        bad_total = next(k for k, v in cnt.items() if v == 1)
        good_total = next(k for k, v in cnt.items() if v > 1)
        bad_child = children[node][ts.index(bad_total)]

        deeper = dfs(bad_child)
        if deeper is not None:
            return deeper
        return weights[bad_child] + (good_total - bad_total)

    out = dfs(root)
    if out is None:
        raise ValueError("no imbalance detected")
    return out


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
    ap = argparse.ArgumentParser(description="AoC 2017 Day 7 fancy Python")
    ap.add_argument("--part", type=int, required=True, choices=[1, 2])
    ap.add_argument("--input")
    args = ap.parse_args()

    input_path = Path(args.input).resolve() if args.input else default_input_path()
    got_sha = sha256_file(input_path)
    if got_sha != EXPECTED_SHA256:
        raise SystemExit(f"checksum mismatch: {got_sha} != {EXPECTED_SHA256}")

    raw = input_path.read_text(encoding="utf-8")

    t0 = time.perf_counter_ns()
    answer = solve_part1(raw) if args.part == 1 else str(solve_part2(raw))
    runtime_ms = (time.perf_counter_ns() - t0) / 1e6

    expected = EXPECTED_PART1 if args.part == 1 else EXPECTED_PART2
    if answer != expected:
        raise SystemExit(f"answer mismatch for part {args.part}: got {answer!r}, expected {expected!r}")

    print(answer)
    print(f"[python-fancy] day=7 part={args.part} runtime_ms={runtime_ms:.3f}", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
