# Changelog

This changelog tracks major structural/tooling milestones (not day-by-day puzzle
algorithm updates).

## 2026-03-03

- Added/expanded `aoclib` as reusable shared library (`auth`, `year`, `http`,
  `parsing`, `grid`, `search`, `geometry`, `intervals`).
- Refactored repeated logic across years to consume shared helpers (selected
  Manhattan, interval, BFS, and Dijkstra patterns).
- Added static structure auditor: `tools/audit_aoc.py`.
- Added runtime accepted-answer verifier: `tools/verify_all.py`.
- Added canonical answer dataset: `tools/accepted_answers.json`.
- Added answer dataset sync utility: `tools/update_accepted_answers.py`.
- Included 2025 accepted answers (released days) in canonical verification.
- Moved operational scripts from repo root into `tools/`.
- Added unified CLI dispatch: `python -m aoclib ...`.
- Added packaging scaffold with entry points: `pyproject.toml`.
- Added lightweight CI workflow: `.github/workflows/ci-lite.yml`.
- Added scaffolding scripts:
  - `tools/new_year.py`
  - `tools/new_day.py`
- Updated `new_year` to support released-day auto-detection with offline
  fallback.
- Added `Makefile` shortcuts (`audit`, `verify`, `sync-answers`, etc.).
- Standardized/expanded documentation:
  - root `README.md`
  - `tools/README.md`
  - `aoclib/README.md`
  - `advent2025/README.md`
  - `tools/VERIFICATION_REPORT.md`
  - `docs/ARCHITECTURE.md`
  - `docs/MAINTENANCE.md`

## Notes

- OCR-output day/part cases are explicitly handled in verifier logic to map
  ASCII-art outputs to accepted decoded answers stored in README tables.
- Some optional solver dependencies were replaced or supplemented with
  dependency-free logic to improve portability.
