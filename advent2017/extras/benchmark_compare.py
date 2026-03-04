#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
YEAR_ROOT = ROOT.parent
DAYS = list(range(1, 26))
PARTS = [1, 2]
LANGS = ("Python", "Bash", "Go", "Rust", "C++")

PAT = re.compile(r"runtime_ms=([0-9]+(?:\.[0-9]+)?)")
ANS_PAT = re.compile(r"- Day (\d+): Part 1 = `([^`]+)`(?:, Part 2 = `([^`]+)`)?")
ROW_PAT = re.compile(
    r"^\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*`([^`]*)`\s*\|\s*([0-9.]+)\s*\|\s*([0-9.]+)\s*\|\s*([0-9.]+)\s*\|\s*([0-9.]+)\s*\|\s*([0-9.]+)\s*\|$"
)


def run_cmd(cmd: list[str]) -> tuple[str, float]:
    t0 = time.perf_counter_ns()
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"cmd failed: {' '.join(cmd)}\n{p.stderr}")
    ans = (p.stdout or "").strip().splitlines()[0]
    m = PAT.search((p.stderr or ""))
    if m:
        ms = float(m.group(1))
    else:
        ms = (time.perf_counter_ns() - t0) / 1e6
    return ans, ms


def load_expected_answers() -> dict[tuple[int, int], str]:
    expected: dict[tuple[int, int], str] = {}
    readme = YEAR_ROOT / "README.md"
    for line in readme.read_text(encoding="utf-8").splitlines():
        m = ANS_PAT.match(line.strip())
        if not m:
            continue
        day = int(m.group(1))
        p1 = m.group(2)
        p2 = m.group(3)
        expected[(day, 1)] = p1
        if p2 is not None:
            expected[(day, 2)] = p2
    return expected


def task_cmd(day: int, part: int, inp: Path, lang: str) -> list[str]:
    if lang == "Python":
        return ["python3", str(ROOT / "python" / "days" / f"day{day}.py"), "--part", str(part), "--input", str(inp)]
    if lang == "Bash":
        return ["bash", str(ROOT / "bash" / "days" / f"day{day}.sh"), "--part", str(part), "--input", str(inp)]
    if lang == "Go":
        return [str(ROOT / "go" / "bin" / f"day{day:02d}"), "--part", str(part), "--input", str(inp)]
    if lang == "Rust":
        return [str(ROOT / "rust" / "target" / "release" / f"day{day:02d}"), "--part", str(part), "--input", str(inp)]
    if lang == "C++":
        return [str(ROOT / "cxx" / "build" / f"day{day:02d}"), "--part", str(part), "--input", str(inp)]
    raise RuntimeError(f"unknown lang: {lang}")


def parse_max_workers() -> int:
    # Benchmarks should run one solver process at a time for clean, comparable latency.
    raw = os.environ.get("BENCH_MAX_WORKERS", "1")
    try:
        n = int(raw)
    except ValueError as e:
        raise RuntimeError(f"invalid BENCH_MAX_WORKERS={raw!r}") from e
    if n < 1:
        raise RuntimeError("BENCH_MAX_WORKERS must be >= 1")
    return 1


def parse_langs() -> tuple[str, ...]:
    raw = os.environ.get("BENCH_LANGS", ",".join(LANGS)).strip()
    if not raw:
        raise RuntimeError("BENCH_LANGS cannot be empty")
    langs = tuple(x.strip() for x in raw.split(",") if x.strip())
    bad = [x for x in langs if x not in LANGS]
    if bad:
        raise RuntimeError(f"unknown BENCH_LANGS entries: {bad}")
    if len(set(langs)) != len(langs):
        raise RuntimeError("BENCH_LANGS contains duplicates")
    return langs


def load_existing_times() -> dict[tuple[int, int], dict[str, float]]:
    out: dict[tuple[int, int], dict[str, float]] = {}
    path = ROOT / "BENCHMARK_2017.md"
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ROW_PAT.match(line.strip())
        if not m:
            continue
        d = int(m.group(1))
        p = int(m.group(2))
        out[(d, p)] = {
            "Python": float(m.group(4)),
            "Bash": float(m.group(5)),
            "Go": float(m.group(6)),
            "Rust": float(m.group(7)),
            "C++": float(m.group(8)),
        }
    return out


def main() -> int:
    expected = load_expected_answers()
    run_langs = parse_langs()
    existing = load_existing_times()

    tasks: list[tuple[int, int, str, list[str]]] = []
    for d in DAYS:
        inp = YEAR_ROOT / f"Day{d}" / f"d{d}_input.txt"
        for part in PARTS:
            if (d, part) not in expected:
                if d == 25 and part == 2:
                    continue
                raise RuntimeError(f"missing expected answer day={d} part={part}")
            for lang in run_langs:
                tasks.append((d, part, lang, task_cmd(d, part, inp, lang)))

    results: dict[tuple[int, int], dict[str, tuple[str, float]]] = {}
    _ = parse_max_workers()
    for d, part, lang, cmd in tasks:
        ans, ms = run_cmd(cmd)
        key = (d, part)
        if key not in results:
            results[key] = {}
        results[key][lang] = (ans, ms)

    out_rows = []
    for d in DAYS:
        for part in PARTS:
            if (d, part) not in expected:
                continue
            got = results.get((d, part), {})
            for lang in run_langs:
                if lang not in got:
                    raise RuntimeError(f"missing benchmark result day={d} part={part} lang={lang}")
                if got[lang][0] != expected[(d, part)]:
                    raise RuntimeError(
                        f"known-answer mismatch day={d} part={part} lang={lang}: got {got[lang][0]!r}, expected {expected[(d, part)]!r}"
                    )
            answer = expected[(d, part)]
            prev = existing.get((d, part), {})
            row_ms: dict[str, float] = {}
            for lang in LANGS:
                if lang in got:
                    row_ms[lang] = got[lang][1]
                elif lang in prev:
                    row_ms[lang] = prev[lang]
                else:
                    raise RuntimeError(
                        f"missing timing for day={d} part={part} lang={lang}; run BENCH_LANGS with that lang at least once"
                    )
            out_rows.append(
                (
                    d,
                    part,
                    answer,
                    row_ms["Python"],
                    row_ms["Bash"],
                    row_ms["Go"],
                    row_ms["Rust"],
                    row_ms["C++"],
                )
            )

    md = [
        "# AoC 2017 Fancy Runtime Comparison",
        "",
        "| Day | Part | Answer | Python ms | Bash ms | Go ms | Rust ms | C++ ms |",
        "|---:|---:|---|---:|---:|---:|---:|---:|",
    ]
    for d, p, a, py, ba, go, rs, cc in out_rows:
        md.append(f"| {d} | {p} | `{a}` | {py:.3f} | {ba:.3f} | {go:.3f} | {rs:.3f} | {cc:.3f} |")

    out = ROOT / "BENCHMARK_2017.md"
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
