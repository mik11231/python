#!/usr/bin/env python3
"""Scaffold a new Advent year folder with README and day directories."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]


def make_year_readme(year_dir: Path, year: int) -> None:
    """
    Run `make_year_readme` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: year_dir, year.
    - Returns the computed result for this stage of the pipeline.
    """
    text = f"""# Advent of Code {year}

This folder follows the same day-based layout as other `advent20XX` folders.

## Structure

- `DayN/dN_input.txt`: puzzle input
- `DayN/dN_instructions.html`: puzzle instructions page (saved HTML)
- `DayN/dayN.py`: Part 1 solution
- `DayN/dayN_part2.py`: Part 2 solution
- `DayN/test_example.py`: AoC example checks (runnable with `python3`)

Tooling and shared library references:

- `../tools/README.md`: detailed CLI/tool documentation
- `../aoclib/README.md`: shared reusable library APIs

## Completed Days

- Fill in accepted answers as stars are completed.
"""
    (year_dir / "README.md").write_text(text, encoding="utf-8")


def detect_released_days(year: int, timeout: int = 15) -> int | None:
    """Return number of released days on adventofcode.com for a given year."""
    url = f"https://adventofcode.com/{year}"
    headers = {"User-Agent": "AOC-New-Year-Scaffold/1.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
    except Exception:
        return None

    days = [int(m) for m in re.findall(rf'href="/{year}/day/(\d+)"', resp.text)]
    if not days:
        return None
    return max(days)


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
    parser = argparse.ArgumentParser(description="Create new adventYYYY folder and optional Day1..Day25.")
    parser.add_argument("year", type=int)
    parser.add_argument("--days", type=int, help="How many day folders to create (auto-detect if omitted)")
    parser.add_argument("--offline-default", type=int, default=25, help="Fallback day count when auto-detect fails")
    parser.add_argument("--force", action="store_true", help="Allow existing year directory")
    args = parser.parse_args(argv)

    year_dir = ROOT / f"advent{args.year}"
    if year_dir.exists() and not args.force:
        raise SystemExit(f"{year_dir} already exists. Use --force to continue.")

    year_dir.mkdir(parents=True, exist_ok=True)
    make_year_readme(year_dir, args.year)

    if args.days is not None:
        day_count = args.days
    else:
        detected = detect_released_days(args.year)
        day_count = detected if detected is not None else args.offline_default
        source = "website" if detected is not None else f"offline-default ({args.offline_default})"
        print(f"Using day count {day_count} from {source}.")

    for d in range(1, day_count + 1):
        day_dir = year_dir / f"Day{d}"
        day_dir.mkdir(parents=True, exist_ok=True)

    print(f"Scaffolded {year_dir} with Day1..Day{day_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
