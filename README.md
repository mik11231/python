# Advent of Code Monorepo

Python solutions and tooling for multiple Advent of Code years.

## Repository Layout

- `advent2015` through `advent2025`: year folders
- `advent20XX/DayN`: day-level solutions and inputs
- `aoclib`: shared utilities for AoC tooling and future solution reuse
- `tools`: operational and quality tooling scripts (download, submit, scaffold,
  audit, style lint, verify, answer sync, diagnostics)
- `tools/accepted_answers.json`: canonical accepted answers used by verifier
- `tools/README.md`: detailed reference for all tooling scripts
- `tools/VERIFICATION_REPORT.md`: latest full-run verification snapshot
- `pyproject.toml`: package metadata and console entry points

## Return-After-Years Starter

If you are coming back after a long break, run these first:

```bash
make help
python -m aoclib --help
make audit
make lint-style
make verify
```

Then read:

- `docs/MAINTENANCE.md` for runbook/checklists
- `tools/README.md` for every script and CLI equivalent
- `docs/ARCHITECTURE.md` for how components fit together

## Year Coverage

- `advent2015`: complete (Day 1-25)
- `advent2016`: complete (Day 1-25)
- `advent2017`: complete (Day 1-25)
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
python -m aoclib lint-style --year 2022
python -m aoclib lint-style --strict --year 2022
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
aoc lint-style --year 2022
aoc new-year 2026
aoc new-day 2026 1
```

Installed console script aliases also exist for common operations:

```bash
aoc-verify --year 2025 --timeout 240
aoc-audit
aoc-sync-answers
aoc-new-year 2026
aoc-new-day 2026 1
```

## Tool Index

Canonical command families:

- Session/auth:
  - `python -m aoclib encode-session`
  - `python -m aoclib test-session`
- Download/submit:
  - `python -m aoclib download-input <day> [year] [base_dir]`
  - `python -m aoclib download-instructions <day> [year] [base_dir]`
  - `python -m aoclib submit <day> <part> <answer> [year]`
- Scaffolding:
  - `python -m aoclib new-year <year> [--days N] [--offline-default N] [--force]`
  - `python -m aoclib new-day <year> <day>`
- Quality/verification:
  - `python -m aoclib audit [paths...]`
  - `python -m aoclib lint-style [--strict] [--year YYYY ...]`
  - `python -m aoclib verify [--year YYYY ...] [--timeout SEC]`
  - `python -m aoclib sync-answers`
- Diagnostics:
  - `python -m aoclib test-download`
  - `python -m aoclib quick-test`

The exhaustive script-level reference with direct command equivalents is in
`tools/README.md`.

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
   - pacing rules:
     - wait `5` seconds between successful submissions
     - wait `60` seconds after any wrong-answer submission before retrying

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
python -m aoclib lint-style --strict
```

This linter enforces lightweight repo conventions:

- year README format and required sections
- Day folder naming and required `dayN.py` part 1 file
- module docstrings and solve entrypoints in day scripts
- strict mode also fails on warnings and is used in CI


## Quick Commands

```bash
make help
make audit
make lint-style
make lint-style YEAR=2022
make lint-style-strict YEAR=2022
make verify
make verify YEAR=2025
make sync-answers
```


## Docs

- `docs/ARCHITECTURE.md`: system layout and component relationships
- `docs/MAINTENANCE.md`: operational runbook/checklists
- `docs/CHANGELOG.md`: major structural/tooling milestones

## Year Architecture and Methodology Index

- [2015](advent2015/README.md): architecture, methodology, theme/story, and solved-scope summary
- [2016](advent2016/README.md): architecture, methodology, theme/story, and solved-scope summary
- [2017](advent2017/README.md): architecture, methodology, theme/story, and solved-scope summary
- [2018](advent2018/README.md): architecture, methodology, theme/story, and solved-scope summary
- [2019](advent2019/README.md): architecture, methodology, theme/story, and solved-scope summary
- [2020](advent2020/README.md): architecture, methodology, theme/story, and solved-scope summary
- [2021](advent2021/README.md): architecture, methodology, theme/story, and solved-scope summary
- [2022](advent2022/README.md): architecture, methodology, theme/story, and solved-scope summary
- [2023](advent2023/README.md): architecture, methodology, theme/story, and solved-scope summary
- [2024](advent2024/README.md): architecture, methodology, theme/story, and solved-scope summary
- [2025](advent2025/README.md): architecture, methodology, theme/story, and solved-scope summary
