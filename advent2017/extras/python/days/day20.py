#!/usr/bin/env python3
"""
advent2017/extras/python/days/day20.py

Implementation Notes:
- This module is intentionally documented in depth so the solution can be
  reconstructed from comments/docstrings after long periods away from the code.
- The code follows a parse -> transform -> solve pipeline where applicable.
- Year scope: advent2017.
- Complexity and data-structure tradeoffs are described in function docstrings below.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import re
import time
from collections import defaultdict
from pathlib import Path

EXPECTED_SHA = "9480ad6f4d423780a0542e172e614170ec28d3eb06c80b7c2b452c6ceeecbfb0"
EXPECTED_PART1 = "144"
EXPECTED_PART2 = "477"
LINE_RE = re.compile(
    r"p=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>, "
    r"v=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>, "
    r"a=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>"
)


def resolve_input(provided: str | None) -> Path:
    """
    Run `resolve_input` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: provided.
    - Returns the computed result for this stage of the pipeline.
    """
    if provided:
        return Path(provided).resolve()
    for c in (
        "advent2017/Day20/d20_input.txt",
        "Day20/d20_input.txt",
        "../Day20/d20_input.txt",
        "../../Day20/d20_input.txt",
    ):
        p = Path(c)
        if p.exists():
            return p.resolve()
    raise SystemExit("input not found")


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


def parse(text: str) -> list[tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]]:
    """
    Run `parse` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: text.
    - Returns the computed result for this stage of the pipeline.
    """
    out = []
    for line in text.splitlines():
        if not line.strip():
            continue
        m = LINE_RE.fullmatch(line.strip())
        if not m:
            raise ValueError(f"bad line: {line!r}")
        nums = tuple(map(int, m.groups()))
        out.append(((nums[0], nums[1], nums[2]), (nums[3], nums[4], nums[5]), (nums[6], nums[7], nums[8])))
    return out


def part1(ps: list[tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]]) -> int:
    """
    Run `part1` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: ps.
    - Returns the computed result for this stage of the pipeline.
    """
    def key(item: tuple[int, tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]]) -> tuple[int, int, int, int]:
        """
        Run `key` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: item.
        - Returns the computed result for this stage of the pipeline.
        """
        i, (p, v, a) = item
        return (
            abs(a[0]) + abs(a[1]) + abs(a[2]),
            abs(v[0]) + abs(v[1]) + abs(v[2]),
            abs(p[0]) + abs(p[1]) + abs(p[2]),
            i,
        )

    return min(enumerate(ps), key=key)[0]


def solve_axis(dp: int, dv: int, da: int) -> tuple[bool, set[int]]:
    # Equation: da*t^2 + (da + 2*dv)*t + 2*dp = 0, t in Z, t >= 0
    """
    Run `solve_axis` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: dp, dv, da.
    - Returns the computed result for this stage of the pipeline.
    """
    if da == 0 and dv == 0:
        if dp == 0:
            return True, set()
        return False, set()
    if da == 0:
        num = -dp
        den = dv
        if den != 0 and num % den == 0:
            t = num // den
            if t >= 0:
                return False, {t}
        return False, set()

    b = da + 2 * dv
    c = 2 * dp
    disc = b * b - 4 * da * c
    if disc < 0:
        return False, set()
    s = math.isqrt(disc)
    if s * s != disc:
        return False, set()
    out: set[int] = set()
    den = 2 * da
    for num in (-b + s, -b - s):
        if den != 0 and num % den == 0:
            t = num // den
            if t >= 0:
                out.add(t)
    return False, out


def position_at(p: tuple[int, int, int], v: tuple[int, int, int], a: tuple[int, int, int], t: int) -> tuple[int, int, int]:
    """
    Run `position_at` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: p, v, a, t.
    - Returns the computed result for this stage of the pipeline.
    """
    return (
        p[0] + v[0] * t + a[0] * t * (t + 1) // 2,
        p[1] + v[1] * t + a[1] * t * (t + 1) // 2,
        p[2] + v[2] * t + a[2] * t * (t + 1) // 2,
    )


def pair_collision_times(pi, pj) -> set[int]:
    """
    Run `pair_collision_times` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: pi, pj.
    - Returns the computed result for this stage of the pipeline.
    """
    (p1, v1, a1) = pi
    (p2, v2, a2) = pj
    axis_any = []
    axis_sets = []
    for k in range(3):
        any_t, ts = solve_axis(p1[k] - p2[k], v1[k] - v2[k], a1[k] - a2[k])
        axis_any.append(any_t)
        axis_sets.append(ts)
    concrete = [s for any_t, s in zip(axis_any, axis_sets) if not any_t]
    if not concrete:
        return set()
    tset = set(concrete[0])
    for s in concrete[1:]:
        tset &= s
    return {t for t in tset if t >= 0}


def part2(ps: list[tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]]) -> int:
    """
    Run `part2` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: ps.
    - Returns the computed result for this stage of the pipeline.
    """
    n = len(ps)
    events: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for i in range(n):
        for j in range(i + 1, n):
            ts = pair_collision_times(ps[i], ps[j])
            for t in ts:
                events[t].append((i, j))

    alive = set(range(n))
    for t in sorted(events):
        involved = set()
        for i, j in events[t]:
            if i in alive and j in alive:
                involved.add(i)
                involved.add(j)
        if len(involved) < 2:
            continue
        groups: dict[tuple[int, int, int], list[int]] = defaultdict(list)
        for i in involved:
            p, v, a = ps[i]
            groups[position_at(p, v, a, t)].append(i)
        for ids in groups.values():
            if len(ids) > 1:
                for i in ids:
                    alive.discard(i)
    return len(alive)


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
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", type=int, choices=[1, 2], required=True)
    ap.add_argument("--input")
    args = ap.parse_args()

    in_path = resolve_input(args.input)
    if sha256_file(in_path) != EXPECTED_SHA:
        raise SystemExit("checksum mismatch")
    ps = parse(in_path.read_text(encoding="utf-8"))

    t0 = time.perf_counter_ns()
    ans = str(part1(ps) if args.part == 1 else part2(ps))
    ms = (time.perf_counter_ns() - t0) / 1e6

    expected = EXPECTED_PART1 if args.part == 1 else EXPECTED_PART2
    if ans != expected:
        raise SystemExit(f"answer mismatch: got {ans}, expected {expected}")
    print(ans)
    print(f"[python-fancy] day=20 part={args.part} runtime_ms={ms:.3f}", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
