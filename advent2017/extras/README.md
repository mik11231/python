# Advent 2017 Extras

Per-day overengineered solution implementations in each language.

- `python/days/dayN.py` (N=1..25)
- `bash/days/dayN.sh` (N=1..25)
- `go/cmd/dayNN/main.go` + `go/bin/dayNN`
- `rust/src/bin/dayNN.rs` + `rust/target/release/dayNN`
- `cxx/src/days/dayNN.cpp` + `cxx/build/dayNN`

Each day executable/script:
- accepts `--part 1|2` and optional `--input`
- validates day input SHA-256
- computes answers algorithmically (no answer tables)
- prints answer to stdout
- prints runtime telemetry to stderr (`runtime_ms=...`)

## Architecture

- One independently runnable solver per language per day.
- Language implementations stay native (no shelling out to another solver language).
- Shared behavior contract: identical CLI shape + input validation + deterministic output.
- Benchmark orchestration runs one solver process at a time for stable comparisons.

## Build

```bash
bash build_all.sh
```

Notes:
- C++ builds run in `Release` mode with aggressive optimization flags and IPO/LTO when supported.
- Rust release profile is tuned for runtime (`lto = "fat"`, `codegen-units = 1`, `panic = "abort"`).
- Go builds use optimized release binaries under `go/bin/`.

## Benchmarking

Generate runtime comparison chart:

```bash
python3 benchmark_compare.py
```

Optional language subset refresh while preserving prior columns:

```bash
BENCH_LANGS=python,go,rust,cxx python3 benchmark_compare.py
```
