# Advent of Code 2019

Fresh 2019 workspace completed end-to-end.

## Structure
- `DayN/dN_input.txt`: puzzle input
- `DayN/dN_instructions.html`: puzzle page snapshot
- `DayN/dayN.py`: Part 1 solution
- `DayN/dayN_part2.py`: Part 2 solution

All listed answers were submitted and accepted for Advent of Code 2019.

## Completed Days
- Day 1: Part 1 = `3331523`, Part 2 = `4994396`
- Day 2: Part 1 = `6568671`, Part 2 = `3951`
- Day 3: Part 1 = `1983`, Part 2 = `107754`
- Day 4: Part 1 = `1330`, Part 2 = `876`
- Day 5: Part 1 = `12234644`, Part 2 = `3508186`
- Day 6: Part 1 = `254447`, Part 2 = `445`
- Day 7: Part 1 = `34852`, Part 2 = `44282086`
- Day 8: Part 1 = `1935`, Part 2 = `CFLUL`
- Day 9: Part 1 = `2436480432`, Part 2 = `45710`
- Day 10: Part 1 = `227`, Part 2 = `604`
- Day 11: Part 1 = `2226`, Part 2 = `HBGLZKLF`
- Day 12: Part 1 = `13500`, Part 2 = `278013787106916`
- Day 13: Part 1 = `180`, Part 2 = `8777`
- Day 14: Part 1 = `1046184`, Part 2 = `1639374`
- Day 15: Part 1 = `216`, Part 2 = `326`
- Day 16: Part 1 = `74608727`, Part 2 = `57920757`
- Day 17: Part 1 = `2804`, Part 2 = `833429`
- Day 18: Part 1 = `3962`, Part 2 = `1844`
- Day 19: Part 1 = `158`, Part 2 = `6191165`
- Day 20: Part 1 = `590`, Part 2 = `7180`
- Day 21: Part 1 = `19359969`, Part 2 = `1140082748`
- Day 22: Part 1 = `5540`, Part 2 = `6821410630991`
- Day 23: Part 1 = `23701`, Part 2 = `17225`
- Day 24: Part 1 = `18400817`, Part 2 = `1944`
- Day 25: Part 1 = `2147502592` (no separate computational Part 2 in AoC 2019)

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

- Theme: Space mission operations with Intcode virtual machines as a recurring computational substrate.
- Story Summary: The 2019 set repeatedly expands an interpreter/runtime ecosystem, then applies it to robotics, mapping, signal processing, and search problems.

## What Our Solutions Addressed

- Correctness: each day/part implementation matches accepted AoC outputs recorded in this README.
- Maintainability: consistent file naming/layout keeps long-term navigation predictable.
- Operability: scripts integrate with repo tooling for download, verify, style lint, and answer synchronization.
