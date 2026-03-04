#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import time
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

EXPECTED_SHA = "48a139f917d7dac161171c28f578d923b212c10108c92bbe05a971f6d8b4fb05"
EXPECTED_PART1 = "1656"
EXPECTED_PART2 = "1642"


def resolve_input(provided: str | None) -> Path:
    if provided:
        return Path(provided).resolve()
    for c in (
        "advent2017/Day24/d24_input.txt",
        "Day24/d24_input.txt",
        "../Day24/d24_input.txt",
        "../../Day24/d24_input.txt",
    ):
        p = Path(c)
        if p.exists():
            return p.resolve()
    raise SystemExit("input not found")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse(text: str) -> tuple[list[tuple[int, int]], dict[int, list[int]]]:
    comps: list[tuple[int, int]] = []
    by_port: dict[int, list[int]] = defaultdict(list)
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        a, b = map(int, s.split("/"))
        idx = len(comps)
        comps.append((a, b))
        by_port[a].append(idx)
        if b != a:
            by_port[b].append(idx)
    return comps, by_port


def solve(comps: list[tuple[int, int]], by_port: dict[int, list[int]]) -> tuple[int, int]:
    by_port_t = {k: tuple(v) for k, v in by_port.items()}

    @lru_cache(maxsize=None)
    def dfs(port: int, used_mask: int) -> tuple[int, int, int]:
        best_strength = 0
        best_len = 0
        best_len_strength = 0
        for idx in by_port_t.get(port, ()):
            if (used_mask >> idx) & 1:
                continue
            a, b = comps[idx]
            nxt = b if a == port else a
            s = a + b
            child_s, child_l, child_ls = dfs(nxt, used_mask | (1 << idx))

            cand_s = s + child_s
            if cand_s > best_strength:
                best_strength = cand_s

            cand_l = 1 + child_l
            cand_ls = s + child_ls
            if cand_l > best_len or (cand_l == best_len and cand_ls > best_len_strength):
                best_len = cand_l
                best_len_strength = cand_ls
        return best_strength, best_len, best_len_strength

    p1, _, p2 = dfs(0, 0)
    return p1, p2


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", type=int, choices=[1, 2], required=True)
    ap.add_argument("--input")
    args = ap.parse_args()

    in_path = resolve_input(args.input)
    if sha256_file(in_path) != EXPECTED_SHA:
        raise SystemExit("checksum mismatch")
    comps, by_port = parse(in_path.read_text(encoding="utf-8"))

    t0 = time.perf_counter_ns()
    p1, p2 = solve(comps, by_port)
    ans = str(p1 if args.part == 1 else p2)
    ms = (time.perf_counter_ns() - t0) / 1e6

    expected = EXPECTED_PART1 if args.part == 1 else EXPECTED_PART2
    if ans != expected:
        raise SystemExit(f"answer mismatch: got {ans}, expected {expected}")
    print(ans)
    print(f"[python-fancy] day=24 part={args.part} runtime_ms={ms:.3f}", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
