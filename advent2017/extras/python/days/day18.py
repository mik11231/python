#!/usr/bin/env python3
"""AoC 2017 Day 18 fancy Python implementation (duet VM)."""

from __future__ import annotations

import argparse
import hashlib
import time
from collections import deque
from pathlib import Path

EXPECTED_SHA256 = "4052bdd33baaf7be897365aa3ad1cff5fae76ade4c474c9e5ebcdf5058ad368e"
EXPECTED_PART1 = "7071"
EXPECTED_PART2 = "8001"


def default_input_path() -> Path:
    cands = [
        Path("advent2017/Day18/d18_input.txt"),
        Path("Day18/d18_input.txt"),
        Path("../Day18/d18_input.txt"),
        Path("../../Day18/d18_input.txt"),
        Path(__file__).resolve().parents[2] / "Day18" / "d18_input.txt",
    ]
    for c in cands:
        if c.exists():
            return c.resolve()
    raise FileNotFoundError("input not found for day 18")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse(raw: str) -> list[tuple[str, str, str | None]]:
    out: list[tuple[str, str, str | None]] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        p = line.split()
        out.append((p[0], p[1], p[2] if len(p) > 2 else None))
    return out


def val(tok: str, regs: dict[str, int]) -> int:
    if tok.lstrip("-").isdigit():
        return int(tok)
    return regs.get(tok, 0)


def solve_part1(prog: list[tuple[str, str, str | None]]) -> int:
    regs: dict[str, int] = {}
    ip = 0
    last = 0

    while 0 <= ip < len(prog):
        op, x, y = prog[ip]
        if op == "snd":
            last = val(x, regs)
        elif op == "set":
            regs[x] = val(y or "0", regs)
        elif op == "add":
            regs[x] = regs.get(x, 0) + val(y or "0", regs)
        elif op == "mul":
            regs[x] = regs.get(x, 0) * val(y or "0", regs)
        elif op == "mod":
            regs[x] = regs.get(x, 0) % val(y or "1", regs)
        elif op == "rcv":
            if val(x, regs) != 0:
                return last
        elif op == "jgz":
            if val(x, regs) > 0:
                ip += val(y or "0", regs)
                continue
        ip += 1

    raise RuntimeError("no recovery")


class Proc:
    def __init__(self, pid: int, prog: list[tuple[str, str, str | None]]) -> None:
        self.pid = pid
        self.prog = prog
        self.regs: dict[str, int] = {"p": pid}
        self.ip = 0
        self.inq: deque[int] = deque()
        self.send_count = 0
        self.waiting = False
        self.terminated = False

    def step(self, outq: deque[int]) -> bool:
        if not (0 <= self.ip < len(self.prog)):
            self.terminated = True
            self.waiting = False
            return False

        op, x, y = self.prog[self.ip]

        if op == "snd":
            outq.append(val(x, self.regs))
            self.send_count += 1
            self.ip += 1
            self.waiting = False
            return True
        if op == "set":
            self.regs[x] = val(y or "0", self.regs)
            self.ip += 1
            self.waiting = False
            return True
        if op == "add":
            self.regs[x] = self.regs.get(x, 0) + val(y or "0", self.regs)
            self.ip += 1
            self.waiting = False
            return True
        if op == "mul":
            self.regs[x] = self.regs.get(x, 0) * val(y or "0", self.regs)
            self.ip += 1
            self.waiting = False
            return True
        if op == "mod":
            self.regs[x] = self.regs.get(x, 0) % val(y or "1", self.regs)
            self.ip += 1
            self.waiting = False
            return True
        if op == "rcv":
            if self.inq:
                self.regs[x] = self.inq.popleft()
                self.ip += 1
                self.waiting = False
                return True
            self.waiting = True
            return False
        if op == "jgz":
            if val(x, self.regs) > 0:
                self.ip += val(y or "0", self.regs)
            else:
                self.ip += 1
            self.waiting = False
            return True

        raise ValueError("bad opcode")


def solve_part2(prog: list[tuple[str, str, str | None]]) -> int:
    p0 = Proc(0, prog)
    p1 = Proc(1, prog)

    while True:
        progressed0 = p0.step(p1.inq)
        progressed1 = p1.step(p0.inq)

        if (not progressed0 and not progressed1) and (p0.waiting or p0.terminated) and (p1.waiting or p1.terminated):
            return p1.send_count


def main() -> int:
    ap = argparse.ArgumentParser(description="AoC 2017 Day 18 fancy Python")
    ap.add_argument("--part", type=int, required=True, choices=[1, 2])
    ap.add_argument("--input")
    args = ap.parse_args()

    input_path = Path(args.input).resolve() if args.input else default_input_path()
    got_sha = sha256_file(input_path)
    if got_sha != EXPECTED_SHA256:
        raise SystemExit(f"checksum mismatch: {got_sha} != {EXPECTED_SHA256}")

    prog = parse(input_path.read_text(encoding="utf-8"))

    t0 = time.perf_counter_ns()
    answer = str(solve_part1(prog) if args.part == 1 else solve_part2(prog))
    runtime_ms = (time.perf_counter_ns() - t0) / 1e6

    expected = EXPECTED_PART1 if args.part == 1 else EXPECTED_PART2
    if answer != expected:
        raise SystemExit(f"answer mismatch for part {args.part}: got {answer!r}, expected {expected!r}")

    print(answer)
    print(f"[python-fancy] day=18 part={args.part} runtime_ms={runtime_ms:.3f}", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
