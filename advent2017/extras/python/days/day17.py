#!/usr/bin/env python3
"""AoC 2017 Day 17 fancy Python implementation (spinlock analytics)."""

from __future__ import annotations

import argparse
import hashlib
import sys
import time
from pathlib import Path

EXPECTED_SHA256 = "03a3d955b8799a90f1ff5a39479fde8e618f8ca3282d5b187186f2cf361abd32"
EXPECTED_PART1 = "808"
EXPECTED_PART2 = "47465686"


def _enable_local_opt_sitepackages() -> None:
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
        Path("advent2017/Day17/d17_input.txt"),
        Path("Day17/d17_input.txt"),
        Path("../Day17/d17_input.txt"),
        Path("../../Day17/d17_input.txt"),
        Path(__file__).resolve().parents[2] / "Day17" / "d17_input.txt",
    ]
    for c in cands:
        if c.exists():
            return c.resolve()
    raise FileNotFoundError("input not found for day 17")


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


def solve_part1(step: int) -> int:
    """
    Run `solve_part1` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: step.
    - Returns the computed result for this stage of the pipeline.
    """
    buf = [0]
    pos = 0
    for v in range(1, 2018):
        pos = (pos + step) % len(buf) + 1
        buf.insert(pos, v)
    return buf[(pos + 1) % len(buf)]


def solve_part2(step: int) -> int:
    """
    Run `solve_part2` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: step.
    - Returns the computed result for this stage of the pipeline.
    """
    pos = 0
    val_after_zero = 0
    size = 1
    for v in range(1, 50_000_001):
        pos = (pos + step) % size + 1
        if pos == 1:
            val_after_zero = v
        size += 1
    return val_after_zero


if njit is not None:
    @njit(cache=True)
    def _solve_part2_jit(step: int) -> int:
        """
        Run `_solve_part2_jit` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: step.
        - Returns the computed result for this stage of the pipeline.
        """
        pos = 0
        val_after_zero = 0
        size = 1
        for v in range(1, 50_000_001):
            pos = (pos + step) % size + 1
            if pos == 1:
                val_after_zero = v
            size += 1
        return val_after_zero
else:
    _solve_part2_jit = None


def _precompile_numba() -> None:
    """
    Run `_precompile_numba` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Returns the computed result for this stage of the pipeline.
    """
    if _solve_part2_jit is None:
        return
    try:
        _solve_part2_jit.compile("(int64,)")
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
    ap = argparse.ArgumentParser(description="AoC 2017 Day 17 fancy Python")
    ap.add_argument("--part", type=int, required=True, choices=[1, 2])
    ap.add_argument("--input")
    args = ap.parse_args()

    input_path = Path(args.input).resolve() if args.input else default_input_path()
    got_sha = sha256_file(input_path)
    if got_sha != EXPECTED_SHA256:
        raise SystemExit(f"checksum mismatch: {got_sha} != {EXPECTED_SHA256}")

    step = int(input_path.read_text(encoding="utf-8").strip())

    if args.part == 2:
        _precompile_numba()
    t0 = time.perf_counter_ns()
    if args.part == 1:
        answer = str(solve_part1(step))
    else:
        if _solve_part2_jit is not None:
            answer = str(int(_solve_part2_jit(step)))
        else:
            answer = str(solve_part2(step))
    runtime_ms = (time.perf_counter_ns() - t0) / 1e6

    expected = EXPECTED_PART1 if args.part == 1 else EXPECTED_PART2
    if answer != expected:
        raise SystemExit(f"answer mismatch for part {args.part}: got {answer!r}, expected {expected!r}")

    print(answer)
    print(f"[python-fancy] day=17 part={args.part} runtime_ms={runtime_ms:.3f}", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
