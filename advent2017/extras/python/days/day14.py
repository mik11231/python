#!/usr/bin/env python3
"""AoC 2017 Day 14 fancy Python implementation (disk defragmentation analysis)."""

from __future__ import annotations

import argparse
import hashlib
import time
from pathlib import Path

EXPECTED_SHA256 = "354ac7a7409ec19ac2561c95f08ba4d0df1a26cdda409bef5ba594cff685eb0a"
EXPECTED_PART1 = "8074"
EXPECTED_PART2 = "1212"
SUFFIX = (17, 31, 73, 47, 23)
BYTE_POPCOUNT = tuple(i.bit_count() for i in range(256))
BYTE_MASK_LE = tuple(
    sum(((i >> (7 - b)) & 1) << b for b in range(8))
    for i in range(256)
)
RING_BASE = tuple(range(256))
ROW_SUFFIXES = tuple(tuple(ord(c) for c in str(i)) + SUFFIX for i in range(128))


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
        Path("advent2017/Day14/d14_input.txt"),
        Path("Day14/d14_input.txt"),
        Path("../Day14/d14_input.txt"),
        Path("../../Day14/d14_input.txt"),
        Path(__file__).resolve().parents[2] / "Day14" / "d14_input.txt",
    ]
    for c in cands:
        if c.exists():
            return c.resolve()
    raise FileNotFoundError("input not found for day 14")


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


def reverse_segment(a: list[int], start: int, length: int) -> None:
    """
    Run `reverse_segment` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: a, start, length.
    - Returns the computed result for this stage of the pipeline.
    """
    n = len(a)
    for i in range(length // 2):
        x = (start + i) % n
        y = (start + length - 1 - i) % n
        a[x], a[y] = a[y], a[x]


def knot_row_mask_and_used(lengths: tuple[int, ...]) -> tuple[int, int]:
    """
    Run `knot_row_mask_and_used` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: lengths.
    - Returns the computed result for this stage of the pipeline.
    """
    ring = list(RING_BASE)
    pos = 0
    skip = 0
    rev = reverse_segment
    ring_loc = ring
    for _ in range(64):
        for ln in lengths:
            rev(ring_loc, pos, ln)
            pos = (pos + ln + skip) % 256
            skip += 1

    mask = 0
    used = 0
    for b in range(16):
        off = b * 16
        x = ring[off]
        for j in range(1, 16):
            x ^= ring[off + j]
        mask |= BYTE_MASK_LE[x] << (b * 8)
        used += BYTE_POPCOUNT[x]
    return mask, used


def build_rows(seed: str) -> tuple[list[int], int]:
    """
    Run `build_rows` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: seed.
    - Returns the computed result for this stage of the pipeline.
    """
    rows = [0] * 128
    used_total = 0
    base = tuple(ord(c) for c in seed) + (45,)
    for r in range(128):
        row_mask, row_used = knot_row_mask_and_used(base + ROW_SUFFIXES[r])
        rows[r] = row_mask
        used_total += row_used
    return rows, used_total


def count_regions(rows: list[int]) -> int:
    """
    Run `count_regions` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: rows.
    - Returns the computed result for this stage of the pipeline.
    """
    unseen = rows[:]
    regions = 0

    for r in range(128):
        while unseen[r]:
            regions += 1
            bit = unseen[r] & -unseen[r]
            unseen[r] ^= bit
            stack = [(r, bit)]
            while stack:
                rr, b = stack.pop()

                nb = b << 1
                if nb & unseen[rr]:
                    unseen[rr] ^= nb
                    stack.append((rr, nb))

                nb = b >> 1
                if nb & unseen[rr]:
                    unseen[rr] ^= nb
                    stack.append((rr, nb))

                if rr > 0 and (b & unseen[rr - 1]):
                    unseen[rr - 1] ^= b
                    stack.append((rr - 1, b))
                if rr < 127 and (b & unseen[rr + 1]):
                    unseen[rr + 1] ^= b
                    stack.append((rr + 1, b))
    return regions


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
    ap = argparse.ArgumentParser(description="AoC 2017 Day 14 fancy Python")
    ap.add_argument("--part", type=int, required=True, choices=[1, 2])
    ap.add_argument("--input")
    args = ap.parse_args()

    input_path = Path(args.input).resolve() if args.input else default_input_path()
    got_sha = sha256_file(input_path)
    if got_sha != EXPECTED_SHA256:
        raise SystemExit(f"checksum mismatch: {got_sha} != {EXPECTED_SHA256}")

    seed = input_path.read_text(encoding="utf-8").strip()

    t0 = time.perf_counter_ns()
    rows, p1 = build_rows(seed)
    if args.part == 1:
        answer = str(p1)
    else:
        answer = str(count_regions(rows))
    runtime_ms = (time.perf_counter_ns() - t0) / 1e6

    expected = EXPECTED_PART1 if args.part == 1 else EXPECTED_PART2
    if answer != expected:
        raise SystemExit(f"answer mismatch for part {args.part}: got {answer!r}, expected {expected!r}")

    print(answer)
    print(f"[python-fancy] day=14 part={args.part} runtime_ms={runtime_ms:.3f}", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
