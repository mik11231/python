# Verification Report

Generated: `2026-03-03T18:02:48-08:00`

This report captures the latest repository-wide verification pass after
standardization, tooling unification, and accepted-answer dataset updates
(including Advent of Code 2025 released days).

## Scope

- Runtime answer verification via `tools/verify_all.py`
- Static consistency audit via `tools/audit_aoc.py`
- Compile sanity for `aoclib/` and `tools/`

## Commands and Results

## 1) Runtime accepted-answer verification

```bash
python3 tools/verify_all.py --timeout 240
```

Observed result:

- `checks=366`
- `failures=0`
- `elapsed_sec=177.2`
- `All verified answers matched accepted values.`

Notes:

- `tools/accepted_answers.json` includes years `2018..2025` (2025 released days).
- OCR-output day/part cases are explicitly handled by verifier rules.

## 2) Static audit

```bash
python3 tools/audit_aoc.py
```

Observed result:

- `files: 373`
- `syntax_ok: 373/373`
- `module_docstring: 373/373`
- `solve_entrypoint: 373/373`
- `main_guard: 373/373`
- `All checks passed.`

## 3) Compile sanity

```bash
python3 -m py_compile aoclib/*.py tools/*.py
```

Observed result:

- No compile errors.

## Re-run policy

Re-run this report whenever:

- any `advent20*/Day*/day*.py` solution changes
- `aoclib` APIs change
- `tools/` scripts or `tools/accepted_answers.json` change
