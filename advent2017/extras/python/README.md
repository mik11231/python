# Python Fancy Per-Day Solutions (2017)

These are overengineered per-day Python solution files with explicit architecture comments and runtime telemetry.

## Architecture

- Each `days/dayN.py` is a standalone day entrypoint with native Python algorithms.
- Solvers expose deterministic compute paths for `--part 1|2` and avoid answer lookup tables.
- Runtime wrappers validate input hashes, measure latency, and emit machine-readable timing info.
- Internal code is heavily documented so each transformation step can be reconstructed from comments.

## Usage

```bash
python3 days/day23.py --part 2 --input ../../Day23/d23_input.txt
python3 days/day8.py --part 1
```

Use `--no-strict` to disable answer validation checks when iterating on new implementations.
