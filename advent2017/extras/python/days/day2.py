#!/usr/bin/env python3
"""AoC 2017 Day 2 fancy Python implementation (real algorithms for both parts)."""

from __future__ import annotations

import argparse
import hashlib
import time
from dataclasses import dataclass
from pathlib import Path

EXPECTED_SHA256 = "c64165a1af8ab4877e736a095bde2b22d523468077099fab5a338f53b0059681"
EXPECTED_PART1 = "36174"
EXPECTED_PART2 = "244"


@dataclass(frozen=True)
class Spreadsheet:
    """Dense integer matrix representation for AoC checksum computations."""

    rows: tuple[tuple[int, ...], ...]

    @staticmethod
    def parse(raw: str) -> "Spreadsheet":
        """
        Run `parse` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: raw.
        - Returns the computed result for this stage of the pipeline.
        """
        parsed_rows: list[tuple[int, ...]] = []
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            parsed_rows.append(tuple(int(tok) for tok in line.split()))
        if not parsed_rows:
            raise ValueError("spreadsheet input is empty")
        return Spreadsheet(rows=tuple(parsed_rows))


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
        Path("advent2017/Day2/d2_input.txt"),
        Path("Day2/d2_input.txt"),
        Path("../Day2/d2_input.txt"),
        Path("../../Day2/d2_input.txt"),
        Path(__file__).resolve().parents[2] / "Day2" / "d2_input.txt",
    ]
    for c in cands:
        if c.exists():
            return c.resolve()
    raise FileNotFoundError("input not found for day 2")


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


def solve_part1(sheet: Spreadsheet) -> int:
    # Row checksum: (max - min) summed across all rows.
    """
    Run `solve_part1` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: sheet.
    - Returns the computed result for this stage of the pipeline.
    """
    return sum(max(row) - min(row) for row in sheet.rows)


def solve_part2(sheet: Spreadsheet) -> int:
    # For each row, find the unique evenly-divisible pair.
    """
    Run `solve_part2` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: sheet.
    - Returns the computed result for this stage of the pipeline.
    """
    total = 0
    for row in sheet.rows:
        found = False
        for i, a in enumerate(row):
            for j, b in enumerate(row):
                if i == j:
                    continue
                if b != 0 and a % b == 0:
                    total += a // b
                    found = True
                    break
            if found:
                break
        if not found:
            raise ValueError("row has no evenly divisible pair")
    return total


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
    ap = argparse.ArgumentParser(description="AoC 2017 Day 2 fancy Python")
    ap.add_argument("--part", type=int, required=True, choices=[1, 2])
    ap.add_argument("--input")
    args = ap.parse_args()

    input_path = Path(args.input).resolve() if args.input else default_input_path()
    got_sha = sha256_file(input_path)
    if got_sha != EXPECTED_SHA256:
        raise SystemExit(f"checksum mismatch: {got_sha} != {EXPECTED_SHA256}")

    sheet = Spreadsheet.parse(input_path.read_text(encoding="utf-8"))

    t0 = time.perf_counter_ns()
    if args.part == 1:
        answer = str(solve_part1(sheet))
        expected = EXPECTED_PART1
    else:
        answer = str(solve_part2(sheet))
        expected = EXPECTED_PART2
    runtime_ms = (time.perf_counter_ns() - t0) / 1e6

    if answer != expected:
        raise SystemExit(f"answer mismatch for part {args.part}: got {answer!r}, expected {expected!r}")

    print(answer)
    print(f"[python-fancy] day=2 part={args.part} runtime_ms={runtime_ms:.3f}", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
