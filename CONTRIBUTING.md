# Contributing

This repository is maintained as a long-lived Advent of Code monorepo.
The goal is correctness first, then consistency and reuse.

## Development Flow

1. Make focused changes (day solution, helper, tooling, or docs).
2. Run checks for what you changed.
3. Commit with a message that includes:
   - what changed
   - why it changed
   - how it was validated

## Required Checks

From repo root:

```bash
make audit
make lint-style
```

For solution changes, also run:

```bash
make verify YEAR=YYYY
```

Use full verification for broad refactors:

```bash
make verify
```

## Style and Structure

- Keep year folders in `adventYYYY` format.
- Keep day folders in `DayN` format.
- Keep at least `dayN.py` present for each day folder.
- Add module docstrings to solution scripts.
- Prefer `solve(...)` (or `solve_part1`/`solve_part2`) entrypoints.
- Prefer a `__main__` guard for direct execution.

## Preferred Reuse

- Reuse `aoclib` helpers when possible (`grid`, `search`, `parsing`, `intervals`, `geometry`, `runner`).
- Keep `tools/` scripts generic and year-agnostic unless a problem requires specialization.
- Avoid introducing heavy dependencies when a pure-Python exact approach is practical.

## Adding New Years and Days

Use scaffolding to avoid drift:

```bash
python -m aoclib new-year YYYY
python -m aoclib new-day YYYY D
```

## Documentation Expectations

Update docs when interfaces or workflows change:

- root `README.md` for user-facing workflow changes
- `tools/README.md` for script/CLI behavior changes
- `aoclib/README.md` for shared library API changes
- `docs/MAINTENANCE.md` for operational checklist updates
