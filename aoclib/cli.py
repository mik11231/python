#!/usr/bin/env python3
"""Unified CLI for AoC repository tooling."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"


def run_tool(script_name: str, args: list[str]) -> int:
    """
    Run `run_tool` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: script_name, args.
    - Returns the computed result for this stage of the pipeline.
    """
    script = TOOLS / script_name
    cmd = [sys.executable, str(script), *args]
    proc = subprocess.run(cmd, cwd=ROOT)
    return proc.returncode


def build_parser() -> argparse.ArgumentParser:
    """
    Run `build_parser` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Returns the computed result for this stage of the pipeline.
    """
    parser = argparse.ArgumentParser(prog="aoc", description="Advent of Code unified tooling CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("encode-session", help="Store AoC session cookie in .aoc_session_b64")
    p.set_defaults(func=lambda a: run_tool("encode_aoc_session.py", []))

    p = sub.add_parser("download-input", help="Download puzzle input")
    p.add_argument("day", type=int)
    p.add_argument("year", type=int, nargs="?")
    p.add_argument("base_dir", nargs="?")
    p.set_defaults(func=lambda a: run_tool("download_input.py", [str(x) for x in (a.day, a.year, a.base_dir) if x is not None]))

    p = sub.add_parser("download-instructions", help="Download puzzle instructions HTML")
    p.add_argument("day", type=int)
    p.add_argument("year", type=int, nargs="?")
    p.add_argument("base_dir", nargs="?")
    p.set_defaults(func=lambda a: run_tool("download_instructions.py", [str(x) for x in (a.day, a.year, a.base_dir) if x is not None]))

    p = sub.add_parser("submit", help="Submit an answer")
    p.add_argument("day", type=int)
    p.add_argument("part", type=int)
    p.add_argument("answer")
    p.add_argument("year", type=int, nargs="?")
    p.set_defaults(func=lambda a: run_tool("submit_answer.py", [str(x) for x in (a.day, a.part, a.answer, a.year) if x is not None]))

    p = sub.add_parser("test-session", help="Test .aoc_session_b64 authentication")
    p.set_defaults(func=lambda a: run_tool("test_aoc_session.py", []))

    p = sub.add_parser("test-download", help="Run network/cookie download diagnostics")
    p.set_defaults(func=lambda a: run_tool("test_download.py", []))

    p = sub.add_parser("quick-test", help="Run one authenticated AoC request")
    p.set_defaults(func=lambda a: run_tool("quick_test.py", []))

    p = sub.add_parser("audit", help="Run static consistency audit")
    p.add_argument("paths", nargs="*")
    p.set_defaults(func=lambda a: run_tool("audit_aoc.py", a.paths))

    p = sub.add_parser("lint-style", help="Run lightweight style/convention linter")
    p.add_argument("--strict", action="store_true")
    p.add_argument("--year", action="append", help="Year to lint (repeatable)")
    def _run_lint_style(a: argparse.Namespace) -> int:
        """
        Run `_run_lint_style` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: a.
        - Returns the computed result for this stage of the pipeline.
        """
        args: list[str] = []
        if a.strict:
            args.append("--strict")
        if a.year:
            for y in a.year:
                args.extend(["--year", str(y)])
        return run_tool("lint_aoc_style.py", args)
    p.set_defaults(func=_run_lint_style)

    p = sub.add_parser("verify", help="Run answer verification against accepted answers")
    p.add_argument("--year", action="append", help="Year to verify (repeatable)")
    p.add_argument("--timeout", type=int, default=180)
    def _run_verify(a: argparse.Namespace) -> int:
        """
        Run `_run_verify` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: a.
        - Returns the computed result for this stage of the pipeline.
        """
        args: list[str] = []
        if a.year:
            for y in a.year:
                args.extend(["--year", str(y)])
        args.extend(["--timeout", str(a.timeout)])
        return run_tool("verify_all.py", args)
    p.set_defaults(func=_run_verify)

    p = sub.add_parser("sync-answers", help="Regenerate accepted_answers.json from year READMEs")
    p.set_defaults(func=lambda a: run_tool("update_accepted_answers.py", []))

    p = sub.add_parser("new-year", help="Scaffold a new adventYYYY folder")
    p.add_argument("year", type=int)
    p.add_argument("--days", type=int)
    p.add_argument("--offline-default", type=int, default=25)
    p.add_argument("--force", action="store_true")
    def _run_new_year(a: argparse.Namespace) -> int:
        """
        Run `_run_new_year` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: a.
        - Returns the computed result for this stage of the pipeline.
        """
        args = [str(a.year), "--offline-default", str(a.offline_default)]
        if a.days is not None:
            args.extend(["--days", str(a.days)])
        if a.force:
            args.append("--force")
        return run_tool("new_year.py", args)
    p.set_defaults(func=_run_new_year)

    p = sub.add_parser("new-day", help="Scaffold files for adventYYYY/DayN")
    p.add_argument("year", type=int)
    p.add_argument("day", type=int)
    p.set_defaults(func=lambda a: run_tool("new_day.py", [str(a.year), str(a.day)]))

    return parser


def main(argv: list[str] | None = None) -> int:
    """
    Run `main` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: argv.
    - Returns the computed result for this stage of the pipeline.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
