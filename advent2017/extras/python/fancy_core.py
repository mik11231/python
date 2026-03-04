#!/usr/bin/env python3
"""Fancy execution core for AoC 2017 Python extras."""

from __future__ import annotations

from dataclasses import dataclass
import argparse
import hashlib
import importlib.util
import time
from pathlib import Path
from types import ModuleType


@dataclass(frozen=True)
class DaySpec:
    day: int
    input_sha256: str
    expected_part1: str
    expected_part2: str


class FancyDayRuntime:
    def __init__(self, spec: DaySpec) -> None:
        self.spec = spec
        self.repo_root = Path(__file__).resolve().parents[2]
        self.day_dir = self.repo_root / f"Day{spec.day}"

    def default_input_path(self) -> Path:
        cands = [
            Path(f"advent2017/Day{self.spec.day}/d{self.spec.day}_input.txt"),
            Path(f"Day{self.spec.day}/d{self.spec.day}_input.txt"),
            Path(f"../Day{self.spec.day}/d{self.spec.day}_input.txt"),
            Path(f"../../Day{self.spec.day}/d{self.spec.day}_input.txt"),
            self.day_dir / f"d{self.spec.day}_input.txt",
        ]
        for c in cands:
            if c.exists():
                return c.resolve()
        raise FileNotFoundError(f"input not found for day {self.spec.day}")

    @staticmethod
    def sha256_file(path: Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()

    def _load_module(self, path: Path, name: str) -> ModuleType:
        spec = importlib.util.spec_from_file_location(name, path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"unable to load module from {path}")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def _module_for_part(self, part: int) -> ModuleType:
        fn = f"day{self.spec.day}.py" if part == 1 else f"day{self.spec.day}_part2.py"
        path = self.day_dir / fn
        return self._load_module(path, f"aoc2017_day{self.spec.day}_p{part}")

    def run(self, part: int, input_path: Path, strict: bool) -> str:
        got_sha = self.sha256_file(input_path)
        if got_sha != self.spec.input_sha256:
            raise SystemExit(
                f"checksum mismatch for day {self.spec.day}: {got_sha} != {self.spec.input_sha256}"
            )

        text = input_path.read_text(encoding="utf-8")
        mod = self._module_for_part(part)
        if not hasattr(mod, "solve"):
            raise RuntimeError(f"module for day {self.spec.day} part {part} has no solve()")

        t0 = time.perf_counter_ns()
        out = str(mod.solve(text))
        ms = (time.perf_counter_ns() - t0) / 1e6

        expected = self.spec.expected_part1 if part == 1 else self.spec.expected_part2
        if strict and out != expected:
            raise SystemExit(
                f"answer mismatch day {self.spec.day} part {part}: got {out!r}, expected {expected!r}"
            )

        print(out)
        print(
            f"[python-fancy] day={self.spec.day} part={part} latency_ms={ms:.3f} strict={int(strict)}",
            file=__import__("sys").stderr,
        )
        return out


def run_cli(spec: DaySpec) -> int:
    ap = argparse.ArgumentParser(description=f"AoC 2017 Fancy Python Day {spec.day}")
    ap.add_argument("--part", type=int, choices=[1, 2], required=True)
    ap.add_argument("--input")
    ap.add_argument("--no-strict", action="store_true")
    args = ap.parse_args()

    rt = FancyDayRuntime(spec)
    inp = Path(args.input).resolve() if args.input else rt.default_input_path()
    rt.run(args.part, inp, strict=not args.no_strict)
    return 0
