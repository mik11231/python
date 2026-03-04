# Architecture

This document explains how the repository is structured, how components depend on
one another, and how data/workflows move through the codebase.

If you are returning after a long break, read this file first, then
`docs/MAINTENANCE.md`.

## Goals

The repository is designed for four things:

- solve Advent of Code puzzles across multiple years in a consistent layout
- keep year/day solutions runnable independently
- provide reusable utility code (`aoclib`) instead of duplicating helpers
- provide reusable tooling (`tools`) that can be used across years and projects

## Top-Level Layout

- `advent2018` ... `advent2025`
  - year folders
  - each contains `DayN` subfolders with solution scripts + inputs
- `aoclib`
  - reusable Python library for shared logic
  - used by both tools and selected day solutions
- `tools`
  - operational scripts (download, submit, verify, audit, scaffolding)
  - contains accepted-answer dataset and verification report docs
- `docs`
  - architecture/maintenance/changelog context
- `Makefile`
  - convenient command wrappers
- `pyproject.toml`
  - package metadata and CLI entry points

## Year/Day Contract

The repository assumes a stable day contract:

- folder: `adventYYYY/DayN/`
- input file: `dN_input.txt`
- instructions HTML: `dN_instructions.html`
- part 1 script: `dayN.py`
- part 2 script: `dayN_part2.py` (if relevant/available)

By convention, scripts expose a `solve(...)` entrypoint and an executable
`if __name__ == "__main__":` block.

`tools/audit_aoc.py` enforces these structural assumptions.

## Shared Library (`aoclib`)

`aoclib` contains reusable primitives that appear frequently in AoC work.

Modules:

- `aoclib.auth`
  - `.aoc_session_b64` loading and encoding helpers
- `aoclib.year`
  - year inference from path context
- `aoclib.http`
  - normalized request wrappers for AoC GET/POST calls
- `aoclib.parsing`
  - common input extraction helpers
- `aoclib.grid`
  - 2D grid neighbor/bounds helpers
- `aoclib.search`
  - BFS / Dijkstra distance utilities
- `aoclib.geometry`
  - Manhattan distance helpers
- `aoclib.intervals`
  - merge/coverage/overlap/range parsing helpers
- `aoclib.cli`
  - unified CLI dispatcher for tool scripts

Design constraints:

- pure Python where practical
- no hidden global state
- explicit return values
- utilities should be generic enough for future years or external projects

## Tooling Layer (`tools`)

Operational scripts live under `tools/`.

Core scripts:

- `download_input.py`
- `download_instructions.py`
- `submit_answer.py`
- `encode_aoc_session.py`
- `test_aoc_session.py`
- `test_download.py`
- `quick_test.py`

Quality scripts:

- `audit_aoc.py` (static structural checks)
- `verify_all.py` (runtime answer verification)
- `update_accepted_answers.py` (sync answer dataset from year READMEs)

Scaffolding scripts:

- `new_year.py` (create year folder + day directories)
- `new_day.py` (create files for a new day)

Data files:

- `accepted_answers.json` (canonical verifier expectations)
- `VERIFICATION_REPORT.md` (latest verification snapshot)

## Unified CLI

You can run tooling either as scripts or via unified CLI.

Script style:

```bash
python tools/verify_all.py --timeout 240
```

Unified CLI style:

```bash
python -m aoclib verify --timeout 240
```

After editable install (`pip install -e .`), console entry points are available
(e.g., `aoc`, `aoc-verify`, `aoc-audit`, `aoc-sync-answers`).

## Verification Model

There are two complementary verification layers:

1. Static structure verification
- tool: `tools/audit_aoc.py`
- checks syntax, module docstring, solve entrypoint, main guard

2. Runtime answer verification
- tool: `tools/verify_all.py`
- runs scripts and compares output with `tools/accepted_answers.json`
- includes explicit handling for known OCR-style outputs that print ASCII art

This split keeps checks fast and robust:

- `audit` catches format drift quickly
- `verify` catches behavioral regressions

## Accepted Answers Source of Truth

`tools/accepted_answers.json` is generated from year README answer lists via
`tools/update_accepted_answers.py`.

Flow:

- update year README completed-day answers
- run `python -m aoclib sync-answers`
- run `python -m aoclib verify`

This ensures documentation and verification remain in sync.

## Dependency Philosophy

The repository prefers dependency-light solutions.

When a third-party dependency is optional, fallback logic should exist when
reasonable (example: `advent2025/Day10/day10_part2.py` supports PuLP but has an
internal exact fallback).

Likewise, solutions were adjusted so `advent2023/Day24/day24_part2.py` no longer
requires `sympy` by default.

## Change Safety Rules

For major refactors, always do:

- baseline outputs before refactor
- targeted diff checks for touched scripts
- `audit` run
- `verify` run
- documentation update if behavior/commands changed

## Operational Entry Points

Primary daily commands are intentionally simple:

```bash
make help
make audit
make verify
make verify YEAR=2025
make sync-answers
```

Equivalent unified CLI:

```bash
python -m aoclib audit
python -m aoclib verify --year 2025
python -m aoclib sync-answers
```
