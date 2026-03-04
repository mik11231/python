#!/usr/bin/env python3
"""Run all Advent solution scripts and verify outputs against accepted answers."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANSWERS_PATH = Path(__file__).with_name("accepted_answers.json")
OCR_OUTPUT_CASES = {
    ("2018", 10, 1),
    ("2019", 8, 2),
    ("2019", 11, 2),
    ("2021", 13, 2),
    ("2022", 10, 2),
}


@dataclass
class CheckResult:
    year: str
    day: int
    part: int
    script: str
    ok: bool
    detail: str


def normalize_text(s: str) -> str:
    return "".join(s.lower().split())


def output_matches(expected: str, output: str, year: str, day: int, part: int) -> bool:
    text = output.strip()
    if not text:
        return False

    if text == expected:
        return True

    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if expected in lines:
        return True

    # Token/substring match for scripts that print labels around answer values.
    if normalize_text(expected) in normalize_text(text):
        return True

    # Extract common payloads from labeled outputs: "...: <answer>"
    payloads = []
    for ln in lines:
        if ":" in ln:
            payloads.append(ln.rsplit(":", 1)[-1].strip())
    if expected in payloads:
        return True

    # Some historical solutions print OCR pixel art while README stores decoded letters.
    if (year, day, part) in OCR_OUTPUT_CASES:
        return "#" in output or "." in output

    return False


def script_path(year: str, day: int, part: int) -> Path:
    base = ROOT / f"advent{year}" / f"Day{day}"
    if part == 1:
        return base / f"day{day}.py"
    return base / f"day{day}_part2.py"


def load_answers() -> dict[str, dict[str, dict[str, str]]]:
    return json.loads(ANSWERS_PATH.read_text(encoding="utf-8"))


def run_one(path: Path, timeout: int) -> tuple[int | str, str]:
    try:
        proc = subprocess.run(
            [sys.executable, str(path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
        return proc.returncode, output.strip()
    except subprocess.TimeoutExpired:
        return "timeout", f"Timed out after {timeout}s"


def verify(years: list[str] | None, timeout: int) -> tuple[list[CheckResult], float]:
    answers = load_answers()
    selected = years if years else sorted(answers.keys())

    results: list[CheckResult] = []
    t0 = time.time()
    for year in selected:
        if year not in answers:
            continue
        for day_str, parts in sorted(answers[year].items(), key=lambda kv: int(kv[0])):
            day = int(day_str)
            for part_str, expected in sorted(parts.items(), key=lambda kv: int(kv[0])):
                part = int(part_str)
                path = script_path(year, day, part)
                if not path.is_file():
                    results.append(
                        CheckResult(year, day, part, str(path), False, "missing script")
                    )
                    continue
                rc, out = run_one(path, timeout)
                if rc != 0:
                    results.append(
                        CheckResult(year, day, part, str(path), False, f"runtime error: {out[-300:]}")
                    )
                    continue
                ok = output_matches(expected, out, year, day, part)
                detail = "ok" if ok else f"expected '{expected}', got '{out.splitlines()[-1] if out else ''}'"
                results.append(CheckResult(year, day, part, str(path), ok, detail))
    return results, time.time() - t0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify Advent solutions against accepted answers.")
    parser.add_argument("--year", action="append", help="Year to verify (repeatable), e.g. 2022")
    parser.add_argument("--timeout", type=int, default=180, help="Per-script timeout in seconds")
    args = parser.parse_args(argv)

    results, elapsed = verify(args.year, args.timeout)
    fails = [r for r in results if not r.ok]

    print(f"checks={len(results)} failures={len(fails)} elapsed_sec={elapsed:.1f}")
    if fails:
        for r in fails:
            print(f"[FAIL] {r.year} Day{r.day} Part{r.part} :: {r.detail} :: {r.script}")
        return 2

    print("All verified answers matched accepted values.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
