#!/usr/bin/env python3
"""AoC 2017 Day 5 fancy Python implementation (real algorithms for both parts)."""

from __future__ import annotations

import argparse
import hashlib
import sys
import time
from pathlib import Path

EXPECTED_SHA256 = "e9c74e01657b99ad1be3cedce52f75bb0e2ac9dfb2efca8714f5f2e0910befa6"
EXPECTED_PART1 = "394829"
EXPECTED_PART2 = "31150702"


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
    import numpy as np  # type: ignore
    from numba import njit  # type: ignore
except Exception:  # pragma: no cover
    np = None
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
        Path("advent2017/Day5/d5_input.txt"),
        Path("Day5/d5_input.txt"),
        Path("../Day5/d5_input.txt"),
        Path("../../Day5/d5_input.txt"),
        Path(__file__).resolve().parents[2] / "Day5" / "d5_input.txt",
    ]
    for c in cands:
        if c.exists():
            return c.resolve()
    raise FileNotFoundError("input not found for day 5")


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


def parse_offsets(raw: str) -> list[int]:
    """
    Run `parse_offsets` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: raw.
    - Returns the computed result for this stage of the pipeline.
    """
    return [int(x) for x in raw.splitlines() if x]


def run_program(offsets: list[int], part: int) -> int:
    """
    Run `run_program` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: offsets, part.
    - Returns the computed result for this stage of the pipeline.
    """
    a = offsets
    i = 0
    steps = 0
    n = len(a)
    if part == 1:
        while True:
            if i < 0 or i >= n:
                break
            jump = a[i]
            a[i] = jump + 1
            i += jump
            steps += 1
    else:
        while True:
            if i < 0 or i >= n:
                break
            jump = a[i]
            a[i] = jump - 1 if jump >= 3 else jump + 1
            i += jump
            steps += 1
    return steps


if njit is not None:
    @njit(cache=True)
    def _run_program_part2_jit(a: "np.ndarray") -> int:
        """
        Run `_run_program_part2_jit` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: a.
        - Returns the computed result for this stage of the pipeline.
        """
        i = 0
        steps = 0
        n = a.shape[0]
        while 0 <= i < n:
            jump = a[i]
            if jump >= 3:
                a[i] = jump - 1
            else:
                a[i] = jump + 1
            i += jump
            steps += 1
        return steps
else:
    _run_program_part2_jit = None


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
    if _run_program_part2_jit is None:
        return
    try:
        _run_program_part2_jit.compile("(int64[:],)")
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
    ap = argparse.ArgumentParser(description="AoC 2017 Day 5 fancy Python")
    ap.add_argument("--part", type=int, required=True, choices=[1, 2])
    ap.add_argument("--input")
    args = ap.parse_args()

    input_path = Path(args.input).resolve() if args.input else default_input_path()
    got_sha = sha256_file(input_path)
    if got_sha != EXPECTED_SHA256:
        raise SystemExit(f"checksum mismatch: {got_sha} != {EXPECTED_SHA256}")

    offsets = parse_offsets(input_path.read_text(encoding="utf-8"))

    _precompile_numba()
    t0 = time.perf_counter_ns()
    if args.part == 2 and _run_program_part2_jit is not None and np is not None:
        arr = np.array(offsets, dtype=np.int64)
        answer = str(int(_run_program_part2_jit(arr)))
    else:
        answer = str(run_program(offsets, args.part))
    runtime_ms = (time.perf_counter_ns() - t0) / 1e6

    expected = EXPECTED_PART1 if args.part == 1 else EXPECTED_PART2
    if answer != expected:
        raise SystemExit(f"answer mismatch for part {args.part}: got {answer!r}, expected {expected!r}")

    print(answer)
    print(f"[python-fancy] day=5 part={args.part} runtime_ms={runtime_ms:.3f}", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
