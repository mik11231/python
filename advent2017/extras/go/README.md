# Go X Solver

Native Go per-day binaries with optimized data paths and explicit concurrency where beneficial.

## Architecture

- Day-specific entrypoints live in `cmd/dayNN/main.go`.
- Common parser/runner helpers are colocated for low overhead and strong type safety.
- Binaries print deterministic answers and emit telemetry suitable for comparison charts.

## Usage

```bash
go build -o bin/aoc2017x ./cmd/aoc2017x
./bin/aoc2017x --day 24 --part 2 --input ../../Day24/d24_input.txt
./bin/aoc2017x --all
```
