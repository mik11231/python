#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import math
import time
from pathlib import Path

EXPECTED_SHA = "866b77a4b5e37e19219792c97103a17d24c5f15a9f0bed448c0e6cfd75378beb"
EXPECTED_PART1 = "3969"
EXPECTED_PART2 = "917"


def resolve_input(provided: str | None) -> Path:
    if provided:
        return Path(provided).resolve()
    for c in (
        "advent2017/Day23/d23_input.txt",
        "Day23/d23_input.txt",
        "../Day23/d23_input.txt",
        "../../Day23/d23_input.txt",
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


def parse(text: str) -> list[tuple[str, str, str]]:
    out = []
    for ln in text.splitlines():
        s = ln.strip()
        if s:
            parts = s.split()
            out.append((parts[0], parts[1], parts[2] if len(parts) > 2 else "0"))
    return out


def val(tok: str, regs: dict[str, int]) -> int:
    if tok.lstrip("-").isdigit():
        return int(tok)
    return regs.get(tok, 0)


def part1(prog: list[tuple[str, str, str]]) -> int:
    regs: dict[str, int] = {}
    ip = 0
    muls = 0
    n = len(prog)
    while 0 <= ip < n:
        op, x, y = prog[ip]
        if op == "set":
            regs[x] = val(y, regs)
        elif op == "sub":
            regs[x] = regs.get(x, 0) - val(y, regs)
        elif op == "mul":
            regs[x] = regs.get(x, 0) * val(y, regs)
            muls += 1
        elif op == "jnz":
            if val(x, regs) != 0:
                ip += val(y, regs)
                continue
        ip += 1
    return muls


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = int(math.isqrt(n))
    d = 3
    while d <= r:
        if n % d == 0:
            return False
        d += 2
    return True


def part2(prog: list[tuple[str, str, str]]) -> int:
    # Derived from the instruction stream semantics for AoC 2017 Day 23.
    b0 = int(prog[0][2])
    b = b0 * 100 + 100_000
    c = b + 17_000
    cnt = 0
    for x in range(b, c + 1, 17):
        if not is_prime(x):
            cnt += 1
    return cnt


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", type=int, choices=[1, 2], required=True)
    ap.add_argument("--input")
    args = ap.parse_args()

    in_path = resolve_input(args.input)
    if sha256_file(in_path) != EXPECTED_SHA:
        raise SystemExit("checksum mismatch")
    prog = parse(in_path.read_text(encoding="utf-8"))

    t0 = time.perf_counter_ns()
    ans = str(part1(prog) if args.part == 1 else part2(prog))
    ms = (time.perf_counter_ns() - t0) / 1e6

    expected = EXPECTED_PART1 if args.part == 1 else EXPECTED_PART2
    if ans != expected:
        raise SystemExit(f"answer mismatch: got {ans}, expected {expected}")
    print(ans)
    print(f"[python-fancy] day=23 part={args.part} runtime_ms={ms:.3f}", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
