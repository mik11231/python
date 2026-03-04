# Advent of Code 2023

This folder follows the same day-based layout as `advent2018` through `advent2022`.

## Structure

- `DayN/dN_input.txt`: puzzle input
- `DayN/dN_instructions.html`: puzzle instructions page (saved HTML)
- `DayN/dayN.py`: Part 1 solution
- `DayN/dayN_part2.py`: Part 2 solution
- `DayN/test_example.py`: AoC example checks (runnable with `python3`)

All listed answers were submitted and accepted for Advent of Code 2023.

## Completed Days

- Day 1: Part 1 = `53651`, Part 2 = `53894`
- Day 2: Part 1 = `2551`, Part 2 = `62811`
- Day 3: Part 1 = `540212`, Part 2 = `87605697`
- Day 4: Part 1 = `21919`, Part 2 = `9881048`
- Day 5: Part 1 = `278755257`, Part 2 = `26829166`
- Day 6: Part 1 = `316800`, Part 2 = `45647654`
- Day 7: Part 1 = `251136060`, Part 2 = `249400220`
- Day 8: Part 1 = `12083`, Part 2 = `13385272668829`
- Day 9: Part 1 = `1725987467`, Part 2 = `971`
- Day 10: Part 1 = `6800`, Part 2 = `483`
- Day 11: Part 1 = `9639160`, Part 2 = `752936133304`
- Day 12: Part 1 = `7173`, Part 2 = `29826669191291`
- Day 13: Part 1 = `37561`, Part 2 = `31108`
- Day 14: Part 1 = `109596`, Part 2 = `96105`
- Day 15: Part 1 = `495972`, Part 2 = `245223`
- Day 16: Part 1 = `7979`, Part 2 = `8437`
- Day 17: Part 1 = `861`, Part 2 = `1037`
- Day 18: Part 1 = `48795`, Part 2 = `40654918441248`
- Day 19: Part 1 = `446517`, Part 2 = `130090458884662`
- Day 20: Part 1 = `1020211150`, Part 2 = `238815727638557`
- Day 21: Part 1 = `3740`, Part 2 = `620962518745459`
- Day 22: Part 1 = `465`, Part 2 = `79042`
- Day 23: Part 1 = `2030`, Part 2 = `6390`
- Day 24: Part 1 = `28266`, Part 2 = `786617045860267`
- Day 25: Part 1 = `602151` (no separate computational Part 2 in AoC 2023)

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

- Theme: Calibration and machine workflows with rich interval/range reasoning and directed process pipelines.
- Story Summary: The 2023 season leans into transforming structured records through staged rules, where algorithmic selection and pruning dominate runtime.

## What Our Solutions Addressed

- Correctness: each day/part implementation matches accepted AoC outputs recorded in this README.
- Maintainability: consistent file naming/layout keeps long-term navigation predictable.
- Operability: scripts integrate with repo tooling for download, verify, style lint, and answer synchronization.
