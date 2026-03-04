# Advent of Code 2025

This folder follows the same day-based layout as `advent2018` through `advent2024`.

## Structure

- `DayN/dN_input.txt`: puzzle input
- `DayN/dN_instructions.html`: puzzle instructions page (saved HTML)
- `DayN/dayN.py`: Part 1 solution
- `DayN/dayN_part2.py`: Part 2 solution (where available)
- `DayN/test_example.py`: AoC example checks (runnable with `python3`)

Tooling and shared library references:

- `../tools/README.md`: detailed CLI/tool documentation
- `../aoclib/README.md`: shared reusable library APIs

All listed answers were submitted and accepted for Advent of Code 2025 (released days).

## Completed Days

- Day 1: Part 1 = `1195`, Part 2 = `6770`
- Day 2: Part 1 = `9188031749`, Part 2 = `11323661261`
- Day 3: Part 1 = `17346`, Part 2 = `172981362045136`
- Day 4: Part 1 = `1505`, Part 2 = `9182`
- Day 5: Part 1 = `674`, Part 2 = `352509891817881`
- Day 6: Part 1 = `6635273135233`, Part 2 = `12542543681221`
- Day 7: Part 1 = `1635`, Part 2 = `58097428661390`
- Day 8: Part 1 = `24360`, Part 2 = `2185817796`
- Day 9: Part 1 = `4729332959`, Part 2 = `1474477524`
- Day 10: Part 1 = `524`, Part 2 = `21696`
- Day 11: Part 1 = `506`, Part 2 = `385912350172800`
- Day 12: Part 1 = `408` (Part 2 not available in this folder yet)

## Architecture

- Day-centric boundaries: each `DayN/` directory isolates input, prompt artifact, part 1, part 2, and example checks.
- Shared operational utilities live outside year folders (`aoclib` + `tools`) so puzzle logic remains focused and portable.
- Solution modules favor pure `solve(...)`/`solve_part*` style functions with thin CLI wrappers for reproducible execution.

## Methodology

- Parse once into explicit in-memory structures (lists, dicts, sets, tuples, lightweight dataclasses where useful).
- Encode puzzle rules as deterministic transformations with testable helper functions.
- Prefer asymptotically sound approaches first; then optimize hotspots using caching, pruning, cycle detection, or tighter data layout.
- Validate against AoC examples before running full input and synchronizing accepted answers.

## Theme and Story Summary

- Theme: Current-year active set (partial release): methodology-first implementations prepared for continuing daily expansion.
- Story Summary: The 2025 story is still unfolding; repository structure and solution conventions are set up to absorb each newly released day with minimal drift.

## What Our Solutions Addressed

- Correctness: each day/part implementation matches accepted AoC outputs recorded in this README.
- Maintainability: consistent file naming/layout keeps long-term navigation predictable.
- Operability: scripts integrate with repo tooling for download, verify, style lint, and answer synchronization.
