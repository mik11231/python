#!/usr/bin/env python3
"""Repository-wide Advent of Code consistency auditor.

Checks `advent20XX/DayN/day*.py` files for:
- parseable syntax
- module docstring
- `solve()` function presence
- executable main guard

Usage:
    python tools/audit_aoc.py
    python tools/audit_aoc.py advent2025
"""

from __future__ import annotations

import ast
import sys
from collections import defaultdict
from pathlib import Path


REQUIRED_CHECKS = ("syntax_ok", "module_docstring")
RECOMMENDED_CHECKS = ("solve_entrypoint", "main_guard")


def iter_solution_files(year_dir: Path):
    yield from sorted(year_dir.glob("Day*/day*.py"))


def has_main_guard(source: str) -> bool:
    compact = "".join(source.split())
    return "if__name__=='__main__':" in compact or 'if__name__=="__main__":' in compact


def has_solve_entrypoint(tree: ast.Module) -> bool:
    """Accept `solve()` plus common variants/import aliases used in older files."""
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in {"solve", "solve_part1", "solve_part2"}:
            return True
        if isinstance(node, ast.ImportFrom):
            if any(alias.name == "solve" for alias in node.names):
                return True
    return False


def audit_file(path: Path) -> dict[str, bool | str]:
    src = path.read_text(encoding="utf-8")
    result: dict[str, bool | str] = {k: False for k in REQUIRED_CHECKS + RECOMMENDED_CHECKS}
    result["path"] = str(path)

    try:
        tree = ast.parse(src)
        result["syntax_ok"] = True
    except SyntaxError:
        return result

    result["module_docstring"] = ast.get_docstring(tree) is not None
    result["solve_entrypoint"] = has_solve_entrypoint(tree)
    result["main_guard"] = has_main_guard(src)
    return result


def find_year_dirs(args: list[str]) -> list[Path]:
    if args:
        return [Path(a) for a in args]
    return sorted(Path(".").glob("advent20[0-9][0-9]"))


def main() -> int:
    years = find_year_dirs(sys.argv[1:])
    if not years:
        print("No advent year folders found.")
        return 1

    totals = defaultdict(int)
    failures: list[tuple[str, str]] = []

    for year in years:
        files = list(iter_solution_files(year))
        if not files:
            continue

        print(f"[{year}] files={len(files)}")
        for path in files:
            report = audit_file(path)
            totals["files"] += 1

            for check in REQUIRED_CHECKS + RECOMMENDED_CHECKS:
                if report[check]:
                    totals[check] += 1
                else:
                    failures.append((report["path"], check))

    print("\nSummary")
    print(f"- files: {totals['files']}")
    for check in REQUIRED_CHECKS + RECOMMENDED_CHECKS:
        print(f"- {check}: {totals[check]}/{totals['files']}")

    required_failures = [item for item in failures if item[1] in REQUIRED_CHECKS]
    recommended_failures = [item for item in failures if item[1] in RECOMMENDED_CHECKS]

    if required_failures:
        print("\nFailures (required)")
        for path, check in required_failures:
            print(f"- {path}: missing {check}")

    if recommended_failures:
        print("\nNotes (recommended improvements)")
        for path, check in recommended_failures:
            print(f"- {path}: missing {check}")

    if required_failures:
        return 2

    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
