# Maintenance Guide

This is the practical runbook for maintaining the repository over time.

If you are returning after months/years away, follow this checklist in order.

## 1) Quick re-orientation (5 minutes)

Run from repository root:

```bash
make help
python -m aoclib --help
```

Read:

- `README.md`
- `tools/README.md`
- `docs/ARCHITECTURE.md`

## 2) Health check (before making changes)

```bash
make audit
make verify
```

Expected:

- audit passes all checks
- verify reports zero failures

If verify fails, inspect failures first before changing anything else.

## 3) Day-to-day puzzle workflow

## A) Session setup (if needed)

```bash
python tools/encode_aoc_session.py
python tools/test_aoc_session.py
```

## B) Fetch puzzle files

```bash
python -m aoclib download-input <day> <year>
python -m aoclib download-instructions <day> <year>
```

Equivalent script form:

```bash
python tools/download_input.py <day> <year>
python tools/download_instructions.py <day> <year>
```

## C) Solve and run scripts

```bash
python advent2025/Day12/day12.py
python advent2025/Day12/day12_part2.py
```

## D) Submit answers

```bash
python -m aoclib submit <day> <part> <answer> <year>
```

## E) Update accepted answer records

1. Update `adventYYYY/README.md` completed-day list.
2. Regenerate canonical dataset:

```bash
python -m aoclib sync-answers
```

3. Re-verify:

```bash
make verify YEAR=YYYY
```

## 4) Adding a new year/day

## New year

```bash
python -m aoclib new-year 2026
```

Behavior:

- if `--days` omitted, attempts to auto-detect released day count from AoC site
- if detection fails, uses `--offline-default` (default `25`)

Examples:

```bash
python -m aoclib new-year 2026 --days 12
python -m aoclib new-year 2026 --offline-default 10
```

## New day in existing year

```bash
python -m aoclib new-day 2026 1
```

This creates standard file skeletons and avoids structure drift.

## 5) Refactor safety procedure

When refactoring multiple day scripts or shared helpers:

1. Capture baseline outputs for target scripts.
2. Apply refactor.
3. Re-run target scripts and compare outputs.
4. Run `make audit`.
5. Run `make verify` (or at least affected year).
6. Update docs (`README`, `tools/README`, `aoclib/README`) as needed.

## 6) Common failure patterns

## A) Path/file not found from repo root

Symptom:

- scripts try to open `DayN/dN_input.txt` relative to cwd

Fix:

- prefer `Path(__file__).with_name('dN_input.txt')`

## B) OCR-style outputs mismatch verifier

Symptom:

- script prints grid/ASCII art, README stores decoded letters

Fix:

- keep script output as-is
- ensure verifier OCR-case mapping includes this day/part

## C) Dependency regressions

Symptom:

- missing optional libs like `pulp`/`sympy`

Fix approach:

- prefer dependency-free exact fallback if feasible
- keep docs explicit about optional dependencies

## 7) Release-quality checks before commit

Minimum:

```bash
make audit
make verify
```

Optional but recommended after major changes:

```bash
python tools/update_accepted_answers.py
python tools/verify_all.py --timeout 240
```

## 8) Update verification report snapshot

After significant structural changes, refresh:

- `tools/VERIFICATION_REPORT.md`

Include:

- timestamp
- command set
- check/failure counts
- notable caveats

## 9) Git hygiene recommendations

- avoid sweeping format/noise changes unless intentional
- commit functional changes and docs together
- keep README answer tables and `accepted_answers.json` aligned
- avoid deleting historical scripts unless replaced by audited equivalents

## 10) Long-term maintenance strategy

If returning years later:

1. Run quick health checks (`audit`, `verify`).
2. Refresh `aoclib`/tool docs if interfaces changed.
3. Use scaffolding scripts for any new year/day.
4. Keep accepted-answer dataset authoritative.

This keeps the project understandable and operational with minimal ramp-up.
