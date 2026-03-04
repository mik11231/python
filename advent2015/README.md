# Advent of Code 2015

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

All listed answers were submitted and accepted for Advent of Code 2015.

## Completed Days

- Day 1: Part 1 = `138`, Part 2 = `1771`
- Day 2: Part 1 = `1586300`, Part 2 = `3737498`
- Day 3: Part 1 = `2565`, Part 2 = `2639`
- Day 4: Part 1 = `282749`, Part 2 = `9962624`
- Day 5: Part 1 = `236`, Part 2 = `51`
- Day 6: Part 1 = `400410`, Part 2 = `15343601`
- Day 7: Part 1 = `956`, Part 2 = `40149`
- Day 8: Part 1 = `1371`, Part 2 = `2117`
- Day 9: Part 1 = `141`, Part 2 = `736`
- Day 10: Part 1 = `329356`, Part 2 = `4666278`
- Day 11: Part 1 = `hepxxyzz`, Part 2 = `heqaabcc`
- Day 12: Part 1 = `111754`, Part 2 = `65402`
- Day 13: Part 1 = `709`, Part 2 = `668`
- Day 14: Part 1 = `2696`, Part 2 = `1084`
- Day 15: Part 1 = `13882464`, Part 2 = `11171160`
- Day 16: Part 1 = `213`, Part 2 = `323`
- Day 17: Part 1 = `654`, Part 2 = `57`
- Day 18: Part 1 = `821`, Part 2 = `886`
- Day 19: Part 1 = `518`, Part 2 = `200`
- Day 20: Part 1 = `665280`, Part 2 = `705600`
- Day 21: Part 1 = `111`, Part 2 = `188`
- Day 22: Part 1 = `1269`, Part 2 = `1309`
- Day 23: Part 1 = `170`, Part 2 = `247`
- Day 24: Part 1 = `11266889531`, Part 2 = `77387711`
- Day 25: Part 1 = `19980801` (no separate computational Part 2 in AoC 2015)

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

- Theme: A classic holiday rescue arc: collecting stars while helping Santa stabilize critical systems (floors, lights, routes, molecules, and combat simulations).
- Story Summary: The 2015 narrative centers on restoring holiday operations by solving increasingly varied computational tasks, ending with the weather machine code grid puzzle.

## What Our Solutions Addressed

- Correctness: each day/part implementation matches accepted AoC outputs recorded in this README.
- Maintainability: consistent file naming/layout keeps long-term navigation predictable.
- Operability: scripts integrate with repo tooling for download, verify, style lint, and answer synchronization.
