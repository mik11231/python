# Python Fancy Per-Day Solutions (2017)

These are overengineered per-day Python solution files.

Design:
- each `days/dayN.py` is a standalone day entrypoint
- typed runtime pipeline (`DaySpec`, `FancyDayRuntime`)
- input SHA-256 validation before execution
- dynamic load of canonical day modules (`DayN/dayN.py`, `dayN_part2.py`)
- strict output validation against accepted answer table
- latency telemetry to stderr

Examples:

```bash
python3 days/day23.py --part 2 --input ../../Day23/d23_input.txt
python3 days/day8.py --part 1
```

Use `--no-strict` to disable answer validation checks.
