# Advent of Code Monorepo

Python solutions and tooling for multiple Advent of Code years.

## Repository Layout

- `advent2018` through `advent2025`: year folders
- `advent20XX/DayN`: day-level solutions and inputs
- `aoclib`: shared utilities for AoC tooling and future solution reuse
- tool scripts:
  - `tools/download_input.py`
  - `tools/download_instructions.py`
  - `tools/submit_answer.py`
  - `tools/encode_aoc_session.py`
  - `tools/test_aoc_session.py`
  - `tools/test_download.py`
  - `tools/quick_test.py`
- `tools/audit_aoc.py`: consistency audit across all year/day solution files
- `tools/verify_all.py`: accepted-answer runtime verification across years
- `tools/accepted_answers.json`: canonical accepted answers used by verifier
- `tools/README.md`: detailed reference for all tooling scripts
- `tools/VERIFICATION_REPORT.md`: latest full-run verification snapshot
- `pyproject.toml`: package metadata and console entry points

## Year Coverage

- `advent2018`: complete (Day 1-25)
- `advent2019`: complete (Day 1-25)
- `advent2020`: complete (Day 1-25)
- `advent2021`: complete (Day 1-25)
- `advent2022`: complete (Day 1-25)
- `advent2023`: complete (Day 1-25)
- `advent2024`: complete (Day 1-25)
- `advent2025`: complete through released days (Day 1-12)

## Shared Library (`aoclib`)

`aoclib` centralizes reusable functionality:

- authentication/session cookie handling (`aoclib.auth`)
- AoC year inference (`aoclib.year`)
- HTTP request wrappers (`aoclib.http`)
- parsing helpers (`aoclib.parsing`)
- grid helpers (`aoclib.grid`)
- search/graph helpers (`aoclib.search`)

See `aoclib/README.md` for API details.

## Unified CLI

Use the package CLI from repo root:

```bash
python -m aoclib --help
python -m aoclib verify --year 2025
python -m aoclib audit
python -m aoclib sync-answers
python -m aoclib new-year 2026        # auto-detect released days
python -m aoclib new-day 2026 1
```

After editable install:

```bash
pip install -e .
aoc --help
aoc verify --year 2024
aoc sync-answers
aoc new-year 2026
aoc new-day 2026 1
```

## Quick Start

For a fresh year/day setup with consistent scaffolding:

```bash
# create year folder + Day1..DayN (auto-detect released day count when online)
python -m aoclib new-year 2026

# add a specific day scaffold later
python -m aoclib new-day 2026 7

# pull puzzle artifacts
python -m aoclib download-input 7 2026 advent2026
python -m aoclib download-instructions 7 2026 advent2026
```

## Tooling Reference

The complete CLI reference for repository tooling is in:

- `tools/README.md`

It documents:

- arguments, defaults, and output paths
- expected cookie handling (`.aoc_session_b64`)
- diagnostics/troubleshooting scripts
- audit + verify behavior and exit semantics

## Common Workflow

1. Store session cookie (once):
   - `python tools/encode_aoc_session.py`
2. Download puzzle input:
   - `python tools/download_input.py <day> <year>`
3. Download instructions page:
   - `python tools/download_instructions.py <day> <year>`
4. Run day solutions:
   - `python advent2024/Day7/day7.py`
   - `python advent2024/Day7/day7_part2.py`
5. Submit answer:
   - `python tools/submit_answer.py <day> <part> <answer> <year>`

## Consistency Audit

Run:

```bash
python tools/audit_aoc.py
```

Current required standards enforced by the auditor:

- valid Python syntax
- module docstring present
- solve entrypoint present (`solve`, `solve_part1`, `solve_part2`, or imported `solve`)

`main` guards are also reported as recommended improvements for legacy script-style files.

## Style Lint

Run:

```bash
python -m aoclib lint-style
```

This linter enforces lightweight repo conventions:

- year README format and required sections
- Day folder naming and required `dayN.py` part 1 file
- module docstrings and solve entrypoints in day scripts


## Quick Commands

```bash
make help
make audit
make lint-style
make verify
make verify YEAR=2025
make sync-answers
```


## Docs

- `docs/ARCHITECTURE.md`: system layout and component relationships
- `docs/MAINTENANCE.md`: operational runbook/checklists
- `docs/CHANGELOG.md`: major structural/tooling milestones
