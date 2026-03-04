# Advent of Code 2016

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

## Completed Days

- Day 1: Part 1 = `234`, Part 2 = `113`
- Day 2: Part 1 = `78985`, Part 2 = `57DD8`
- Day 3: Part 1 = `917`, Part 2 = `1649`
- Day 4: Part 1 = `158835`, Part 2 = `993`
- Day 5: Part 1 = `1a3099aa`, Part 2 = `694190cd`
- Day 6: Part 1 = `tsreykjj`, Part 2 = `hnfbujie`
- Day 7: Part 1 = `118`, Part 2 = `260`
- Day 8: Part 1 = `119`, Part 2 = `ZFHFSFOGPO`
- Day 9: Part 1 = `150914`, Part 2 = `11052855125`
- Day 10: Part 1 = `113`, Part 2 = `12803`
- Day 11: Part 1 = `47`, Part 2 = `71`
- Day 12: Part 1 = `318077`, Part 2 = `9227731`
- Day 13: Part 1 = `96`, Part 2 = `141`
- Day 14: Part 1 = `15035`, Part 2 = `19968`
- Day 15: Part 1 = `16824`, Part 2 = `3543984`
- Day 16: Part 1 = `10011010010010010`, Part 2 = `10101011110100011`
- Day 17: Part 1 = `RDRLDRDURD`, Part 2 = `596`
- Day 18: Part 1 = `1956`, Part 2 = `19995121`
- Day 19: Part 1 = `1815603`, Part 2 = `1410630`
- Day 20: Part 1 = `22887907`, Part 2 = `109`
- Day 21: Part 1 = `aefgbcdh`, Part 2 = `egcdahbf`
- Day 22: Part 1 = `946`, Part 2 = `195`
- Day 23: Part 1 = `11748`, Part 2 = `479008308`
- Day 24: Part 1 = `490`, Part 2 = `744`
- Day 25: Part 1 = `198` (no separate computational Part 2 in AoC 2016)

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

- Theme: Infiltration and decoding: navigation, keypads, microchips, and assembly-like interpreters under constraints.
- Story Summary: The 2016 progression focuses on movement through hostile/unknown environments and controlled execution of small virtual machines to recover target signals and credentials.

## What Our Solutions Addressed

- Correctness: each day/part implementation matches accepted AoC outputs recorded in this README.
- Maintainability: consistent file naming/layout keeps long-term navigation predictable.
- Operability: scripts integrate with repo tooling for download, verify, style lint, and answer synchronization.
