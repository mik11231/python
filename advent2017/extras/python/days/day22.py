#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import sys
import time
from pathlib import Path

EXPECTED_SHA = "29581d7567b692271626cc1b3e1448f3456036af5d0bb1e0714fbaf2cf7bc878"
EXPECTED_PART1 = "5246"
EXPECTED_PART2 = "2512059"


def _enable_local_opt_sitepackages() -> None:
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
    from numba import njit, types  # type: ignore
    from numba.typed import Dict  # type: ignore
except Exception:  # pragma: no cover
    np = None
    njit = None
    types = None
    Dict = None


def resolve_input(provided: str | None) -> Path:
    if provided:
        return Path(provided).resolve()
    for c in (
        "advent2017/Day22/d22_input.txt",
        "Day22/d22_input.txt",
        "../Day22/d22_input.txt",
        "../../Day22/d22_input.txt",
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


def parse(text: str) -> set[tuple[int, int]]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    n = len(lines)
    off = n // 2
    inf: set[tuple[int, int]] = set()
    for r, row in enumerate(lines):
        for c, ch in enumerate(row):
            if ch == "#":
                inf.add((r - off, c - off))
    return inf


def parse_packed(text: str) -> list[int]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    n = len(lines)
    off = n // 2
    inf: list[int] = []
    for r, row in enumerate(lines):
        rr = r - off
        for c, ch in enumerate(row):
            if ch == "#":
                cc = c - off
                key = (rr << 32) ^ (cc & 0xFFFFFFFF)
                inf.append(key)
    return inf


def part1(infected0: set[tuple[int, int]]) -> int:
    infected = set(infected0)
    r = c = 0
    dr, dc = -1, 0
    made = 0
    for _ in range(10_000):
        pos = (r, c)
        if pos in infected:
            dr, dc = dc, -dr
            infected.remove(pos)
        else:
            dr, dc = -dc, dr
            infected.add(pos)
            made += 1
        r += dr
        c += dc
    return made


def part2(infected0: set[tuple[int, int]]) -> int:
    # 0 clean, 1 weakened, 2 infected, 3 flagged
    state = {p: 2 for p in infected0}
    r = c = 0
    dr, dc = -1, 0
    made = 0
    for _ in range(10_000_000):
        pos = (r, c)
        s = state.get(pos, 0)
        if s == 0:
            dr, dc = -dc, dr
            state[pos] = 1
        elif s == 1:
            state[pos] = 2
            made += 1
        elif s == 2:
            dr, dc = dc, -dr
            state[pos] = 3
        else:
            dr, dc = -dr, -dc
            state.pop(pos, None)
        r += dr
        c += dc
    return made


if njit is not None and Dict is not None and np is not None:
    @njit(cache=True)
    def _part2_jit(init_keys: "np.ndarray") -> int:
        state = Dict.empty(key_type=types.int64, value_type=types.int8)
        s1 = np.int8(1)
        s2 = np.int8(2)
        s3 = np.int8(3)
        for i in range(init_keys.shape[0]):
            state[int(init_keys[i])] = s2
        r = 0
        c = 0
        d = 0
        made = 0
        for _ in range(10_000_000):
            key = (r << 32) ^ (c & 0xFFFFFFFF)
            if key in state:
                s = state[key]
            else:
                s = 0
            if s == 0:
                d = (d + 3) & 3
                state[key] = s1
            elif s == 1:
                state[key] = s2
                made += 1
            elif s == 2:
                d = (d + 1) & 3
                state[key] = s3
            else:
                d = (d + 2) & 3
                if key in state:
                    del state[key]
            if d == 0:
                r -= 1
            elif d == 1:
                c += 1
            elif d == 2:
                r += 1
            else:
                c -= 1
        return made
else:
    _part2_jit = None


def _precompile_numba() -> None:
    if _part2_jit is None:
        return
    try:
        _part2_jit.compile("(int64[:],)")
    except Exception:
        pass


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", type=int, choices=[1, 2], required=True)
    ap.add_argument("--input")
    args = ap.parse_args()

    in_path = resolve_input(args.input)
    if sha256_file(in_path) != EXPECTED_SHA:
        raise SystemExit("checksum mismatch")
    text = in_path.read_text(encoding="utf-8")
    infected = parse(text)

    t0 = time.perf_counter_ns()
    if args.part == 1:
        ans = str(part1(infected))
    else:
        if _part2_jit is not None and np is not None:
            _precompile_numba()
            init_keys = np.array(parse_packed(text), dtype=np.int64)
            ans = str(int(_part2_jit(init_keys)))
        else:
            ans = str(part2(infected))
    ms = (time.perf_counter_ns() - t0) / 1e6

    expected = EXPECTED_PART1 if args.part == 1 else EXPECTED_PART2
    if ans != expected:
        raise SystemExit(f"answer mismatch: got {ans}, expected {expected}")
    print(ans)
    print(f"[python-fancy] day=22 part={args.part} runtime_ms={ms:.3f}", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
