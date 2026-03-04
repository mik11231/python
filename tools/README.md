# tools

Repository tooling for Advent of Code input download, instruction archiving,
authentication checks, answer submission, and solution consistency audits.

All commands are intended to be run from the repository root.

You can invoke tools either directly (script path) or through the unified CLI:

- Direct: `python tools/<script>.py ...`
- Unified CLI: `python -m aoclib <subcommand> ...` (or `aoc ...` after install)

## Scripts

## `tools/encode_aoc_session.py`

Stores your Advent of Code `session` cookie in base64 form as `.aoc_session_b64`
in the repository root.

- Input: interactive hidden prompt for the raw cookie value
- Output: `.aoc_session_b64` file (git-ignored)
- Notes:
  - Includes a short-cookie warning for accidental truncation
  - Never prints the raw cookie value

Usage:

```bash
python tools/encode_aoc_session.py
```

## `tools/test_aoc_session.py`

Validates that `.aoc_session_b64` decodes and can authenticate against
`/2025/day/1/input`.

- Input: `.aoc_session_b64`
- Output: status summary (`200`, `400`, `404`, etc.)
- Notes:
  - Does not print your cookie
  - Useful to separate auth issues from solver/tool issues

Usage:

```bash
python tools/test_aoc_session.py
```

## `tools/download_input.py`

Downloads puzzle input and writes it into `Day<day>/d<day>_input.txt`.

Arguments:

- `<day>` required, `1..25`
- `[year]` optional; defaults to `infer_default_year(2025)` from cwd
- `[base_dir]` optional; defaults to current directory

Cookie source:

- Only `.aoc_session_b64` in repo root

Usage:

```bash
python tools/download_input.py <day> [year] [base_dir]
python tools/download_input.py 14 2024
python tools/download_input.py 3 2025 advent2025
```

Exit behavior:

- prints explicit HTTP/network error diagnostics
- returns non-success status for invalid arguments or missing cookie

## `tools/download_instructions.py`

Downloads puzzle instruction HTML and writes `Day<day>/d<day>_instructions.html`.

Arguments:

- `<day>` required, `1..25`
- `[year]` optional; defaults to inferred year
- `[base_dir]` optional; defaults to current directory

Cookie source:

- Optional `.aoc_session_b64` (instructions are often public for released days)

Usage:

```bash
python tools/download_instructions.py <day> [year] [base_dir]
python tools/download_instructions.py 14 2024
```

## `tools/submit_answer.py`

Submits an answer for a specific day/part.

Arguments:

- `<day>` required, `1..25`
- `<part>` required, `1` or `2`
- `<answer>` required, string token sent to AoC
- `[year]` optional; defaults to inferred year

Cookie source:

- Required `.aoc_session_b64`

Usage:

```bash
python tools/submit_answer.py <day> <part> <answer> [year]
python tools/submit_answer.py 24 2 786617045860267 2023
```

Response handling:

- detects correct answer
- detects already-completed part
- detects wrong answer/rate limit and parses wait hints where present

## `tools/test_download.py`

Quick non-invasive diagnostics:

- cookie decode check
- `requests` availability sanity
- basic network reachability to adventofcode.com

Usage:

```bash
python tools/test_download.py
```

## `tools/quick_test.py`

Single end-to-end authenticated request against Day 1 input of inferred year.

Usage:

```bash
python tools/quick_test.py
```

## `tools/audit_aoc.py`

Static consistency auditor across all `advent20XX/Day*/day*.py` files.

Checks:

- required:
  - parseable syntax
  - module docstring
- recommended/standardized:
  - solve entrypoint (`solve`, `solve_part1`, `solve_part2`, or imported `solve`)
  - `if __name__ == '__main__'`/double-quote equivalent guard

Usage:

```bash
python tools/audit_aoc.py
python tools/audit_aoc.py advent2025
```

Exit codes:

- `0` required checks pass
- non-zero if required checks fail

## `tools/lint_aoc_style.py`

Lightweight style/convention checker focused on long-term consistency.

Checks:

- year README structure:
  - `# Advent of Code YYYY`
  - `## Completed Days`
- day folder naming (`DayN`) and required part 1 script (`dayN.py`)
- solution script conventions:
  - parseable syntax
  - module docstring
  - solve entrypoint (`solve`, `solve_part1`, `solve_part2`) as warning
- recommended:
  - `if __name__ == "__main__"` main guard (warning by default)

Usage:

```bash
python tools/lint_aoc_style.py
python tools/lint_aoc_style.py --strict
```

Exit codes:

- `0` no errors (warnings allowed unless `--strict`)
- non-zero on style errors (and warnings in `--strict`)

## `tools/accepted_answers.json`

Canonical accepted-answer dataset used by `tools/verify_all.py`.

- Source of truth for expected outputs in automation
- Includes years with completed answer lists
- Updated when README accepted-answer tables are updated

Regenerate from READMEs:

```bash
python tools/update_accepted_answers.py
# or
python -m aoclib sync-answers
```

## `tools/verify_all.py`

Runtime verification against `tools/accepted_answers.json`.

Usage:

```bash
python tools/verify_all.py
python tools/verify_all.py --year 2025 --timeout 240
```

Output:

- total check count
- failure count
- per-failure detail (year/day/part + expected/actual summary)

Known handling:

- OCR-style output days (scripts printing ASCII art) are handled explicitly.

## `tools/update_accepted_answers.py`

Parses `advent20*/README.md` completed-day answer lists and rewrites
`tools/accepted_answers.json`.

Usage:

```bash
python tools/update_accepted_answers.py
```

## `tools/new_year.py`

Scaffolds a new `adventYYYY` folder with README and day directories.

Behavior:

- If `--days` is provided, uses that exact count.
- If `--days` is omitted, attempts to detect released day count from
  `https://adventofcode.com/<year>`.
- If detection fails (offline/network error), falls back to `--offline-default`
  (default: `25`).

Usage:

```bash
python tools/new_year.py 2026
python tools/new_year.py 2026 --days 12
python tools/new_year.py 2026 --offline-default 10
python tools/new_year.py 2026 --force
```

## `tools/new_day.py`

Scaffolds `DayN` files for an existing year:

- `dN_input.txt`
- `dN_instructions.html`
- `dayN.py`
- `dayN_part2.py`
- `test_example.py`

Usage:

```bash
python tools/new_day.py 2026 1
```

## Related Library

These scripts depend on shared primitives from `aoclib`:

- `aoclib.auth` for session decode/encode
- `aoclib.year` for year inference
- `aoclib.http` for consistent AoC request wrappers

See `../aoclib/README.md` for API details.
