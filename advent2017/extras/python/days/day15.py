#!/usr/bin/env python3
"""AoC 2017 Day 15 fancy Python implementation (dueling generators)."""

from __future__ import annotations

import argparse
import hashlib
import sys
import time
from pathlib import Path

EXPECTED_SHA256 = "8d4f35b1950c1ca0bd04c13fe9e4a9a15065f902a86a82606973db0b9fe346f7"
EXPECTED_PART1 = "650"
EXPECTED_PART2 = "336"

FA = 16807
FB = 48271
MOD = 2147483647
MASK = 0xFFFF


def _enable_local_opt_sitepackages() -> None:
    # Allow baseline `python3` invocations to use modules installed in repo-local venv.
    """
    Run `_enable_local_opt_sitepackages` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Returns the computed result for this stage of the pipeline.
    """
    root = Path(__file__).resolve().parents[4]
    lib_dir = root / ".venv-opt" / "lib"
    if not lib_dir.exists():
        return
    for p in lib_dir.glob("python*/site-packages"):
        sp = str(p)
        if sp not in sys.path:
            sys.path.insert(0, sp)


_enable_local_opt_sitepackages()

try:
    from numba import njit  # type: ignore
except Exception:  # pragma: no cover
    njit = None


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
        Path("advent2017/Day15/d15_input.txt"),
        Path("Day15/d15_input.txt"),
        Path("../Day15/d15_input.txt"),
        Path("../../Day15/d15_input.txt"),
        Path(__file__).resolve().parents[2] / "Day15" / "d15_input.txt",
    ]
    for c in cands:
        if c.exists():
            return c.resolve()
    raise FileNotFoundError("input not found for day 15")


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


def parse_seeds(raw: str) -> tuple[int, int]:
    """
    Run `parse_seeds` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: raw.
    - Returns the computed result for this stage of the pipeline.
    """
    vals = [int(line.split()[-1]) for line in raw.splitlines() if line.strip()]
    return vals[0], vals[1]


def solve_part1(a: int, b: int) -> int:
    """
    Run `solve_part1` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: a, b.
    - Returns the computed result for this stage of the pipeline.
    """
    fa = FA
    fb = FB
    mod = MOD
    mask = MASK
    cnt = 0
    for _ in range(40_000_000):
        a = (a * fa) % mod
        b = (b * fb) % mod
        if (a & mask) == (b & mask):
            cnt += 1
    return cnt


def solve_part2(a: int, b: int) -> int:
    """
    Run `solve_part2` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: a, b.
    - Returns the computed result for this stage of the pipeline.
    """
    fa = FA
    fb = FB
    mod = MOD
    mask = MASK
    cnt = 0
    for _ in range(5_000_000):
        while True:
            a = (a * fa) % mod
            if (a & 3) == 0:
                break
        while True:
            b = (b * fb) % mod
            if (b & 7) == 0:
                break
        if (a & mask) == (b & mask):
            cnt += 1
    return cnt


if njit is not None:
    @njit(cache=True)
    def _solve_part1_jit(a: int, b: int) -> int:
        """
        Run `_solve_part1_jit` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: a, b.
        - Returns the computed result for this stage of the pipeline.
        """
        cnt = 0
        for _ in range(40_000_000):
            a = (a * FA) % MOD
            b = (b * FB) % MOD
            if (a & MASK) == (b & MASK):
                cnt += 1
        return cnt

    @njit(cache=True)
    def _solve_part2_jit(a: int, b: int) -> int:
        """
        Run `_solve_part2_jit` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: a, b.
        - Returns the computed result for this stage of the pipeline.
        """
        cnt = 0
        for _ in range(5_000_000):
            while True:
                a = (a * FA) % MOD
                if (a & 3) == 0:
                    break
            while True:
                b = (b * FB) % MOD
                if (b & 7) == 0:
                    break
            if (a & MASK) == (b & MASK):
                cnt += 1
        return cnt
else:
    _solve_part1_jit = None
    _solve_part2_jit = None


def _precompile_numba(part: int) -> None:
    """
    Run `_precompile_numba` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: part.
    - Returns the computed result for this stage of the pipeline.
    """
    try:
        if part == 1 and _solve_part1_jit is not None:
            _solve_part1_jit.compile("(int64,int64)")
        if part == 2 and _solve_part2_jit is not None:
            _solve_part2_jit.compile("(int64,int64)")
    except Exception:
        pass


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
    ap = argparse.ArgumentParser(description="AoC 2017 Day 15 fancy Python")
    ap.add_argument("--part", type=int, required=True, choices=[1, 2])
    ap.add_argument("--input")
    args = ap.parse_args()

    input_path = Path(args.input).resolve() if args.input else default_input_path()
    got_sha = sha256_file(input_path)
    if got_sha != EXPECTED_SHA256:
        raise SystemExit(f"checksum mismatch: {got_sha} != {EXPECTED_SHA256}")

    a0, b0 = parse_seeds(input_path.read_text(encoding="utf-8"))

    _precompile_numba(args.part)
    t0 = time.perf_counter_ns()
    if args.part == 1:
        if _solve_part1_jit is not None:
            answer = str(int(_solve_part1_jit(a0, b0)))
        else:
            answer = str(solve_part1(a0, b0))
    else:
        if _solve_part2_jit is not None:
            answer = str(int(_solve_part2_jit(a0, b0)))
        else:
            answer = str(solve_part2(a0, b0))
    runtime_ms = (time.perf_counter_ns() - t0) / 1e6

    expected = EXPECTED_PART1 if args.part == 1 else EXPECTED_PART2
    if answer != expected:
        raise SystemExit(f"answer mismatch for part {args.part}: got {answer!r}, expected {expected!r}")

    print(answer)
    print(f"[python-fancy] day=15 part={args.part} runtime_ms={runtime_ms:.3f}", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
