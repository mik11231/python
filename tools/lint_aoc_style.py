#!/usr/bin/env python3
"""Lightweight style/convention linter for AoC repository structure."""

from __future__ import annotations

import argparse
import ast
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
YEAR_RE = re.compile(r"^advent(20\d{2})$")
DAY_DIR_RE = re.compile(r"^Day(\d+)$")
SOLUTION_FILE_RE = re.compile(r"^day\d+(?:_part2)?\.py$")


def iter_solution_files(base: Path) -> list[Path]:
    """Return all AoC day solution scripts under year folders."""
    files: list[Path] = []
    for year_dir in sorted(p for p in base.iterdir() if p.is_dir() and YEAR_RE.match(p.name)):
        for day_dir in sorted(p for p in year_dir.iterdir() if p.is_dir() and DAY_DIR_RE.match(p.name)):
            files.extend(
                sorted(
                    p for p in day_dir.glob("day*.py")
                    if SOLUTION_FILE_RE.match(p.name)
                )
            )
    return files


def has_main_guard(source: str) -> bool:
    """Return True if source contains a conventional __main__ guard."""
    return (
        "if __name__ == '__main__':" in source
        or 'if __name__ == "__main__":' in source
    )


def lint_readmes(base: Path, errors: list[str]) -> None:
    """Validate year README shape and required sections."""
    for year_dir in sorted(p for p in base.iterdir() if p.is_dir() and YEAR_RE.match(p.name)):
        year = YEAR_RE.match(year_dir.name).group(1)  # type: ignore[union-attr]
        readme = year_dir / "README.md"
        if not readme.exists():
            errors.append(f"{readme}: missing README.md")
            continue
        text = readme.read_text(encoding="utf-8")
        if f"# Advent of Code {year}" not in text:
            errors.append(f"{readme}: missing '# Advent of Code {year}' heading")
        if "## Completed Days" not in text:
            errors.append(f"{readme}: missing '## Completed Days' section")


def lint_day_structure(base: Path, errors: list[str]) -> None:
    """Validate DayN folder naming and required part 1 file presence."""
    for year_dir in sorted(p for p in base.iterdir() if p.is_dir() and YEAR_RE.match(p.name)):
        for day_dir in sorted(p for p in year_dir.iterdir() if p.is_dir() and p.name.startswith("Day")):
            match = DAY_DIR_RE.match(day_dir.name)
            if not match:
                errors.append(f"{day_dir}: invalid day folder name; expected DayN")
                continue
            day = int(match.group(1))
            part1 = day_dir / f"day{day}.py"
            if not part1.exists():
                errors.append(f"{day_dir}: missing required part1 script {part1.name}")


def lint_python_files(files: list[Path], errors: list[str], warnings: list[str]) -> None:
    """Validate Python module conventions for solution files."""
    for path in files:
        rel = path.relative_to(ROOT)
        source = path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(source, filename=str(path))
        except SyntaxError as exc:
            errors.append(f"{rel}:{exc.lineno}:{exc.offset}: syntax error: {exc.msg}")
            continue

        if not ast.get_docstring(tree):
            errors.append(f"{rel}: missing module docstring")

        solve_names = {"solve", "solve_part1", "solve_part2"}
        has_solve = any(
            isinstance(node, ast.FunctionDef) and node.name in solve_names
            for node in tree.body
        )
        if not has_solve:
            warnings.append(f"{rel}: missing solve entrypoint ({sorted(solve_names)})")

        if not has_main_guard(source):
            warnings.append(f"{rel}: missing __main__ guard (recommended)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint AoC folder/style conventions.")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings too.")
    args = parser.parse_args(argv)

    errors: list[str] = []
    warnings: list[str] = []

    lint_readmes(ROOT, errors)
    lint_day_structure(ROOT, errors)
    lint_python_files(iter_solution_files(ROOT), errors, warnings)

    if errors:
        print("style-errors:")
        for e in errors:
            print(f"  - {e}")
    if warnings:
        print("style-warnings:")
        for w in warnings:
            print(f"  - {w}")
    print(f"style-summary: errors={len(errors)} warnings={len(warnings)}")

    if errors:
        return 1
    if warnings and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
