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
- prints answer to stdout
- prints runtime telemetry to stderr (`runtime_ms=...`)

Build all native artifacts:

```bash
bash build_all.sh

# Notes

- C++ builds run in `Release` mode with aggressive optimization flags and IPO/LTO when supported.
- Rust release profile is tuned for runtime (`lto = "fat"`, `codegen-units = 1`, `panic = "abort"`).
- `native/bin/day15_fast` and `native/bin/day17_fast` are built by `build_all.sh` and used as optional accelerators by Python/Bash day scripts.
- Python/Bash heavy paths for days 20/22/25 can optionally delegate to prebuilt optimized C++ binaries in `cxx/build/` when available, with in-language fallback otherwise.
```

Generate runtime comparison chart:

```bash
python3 benchmark_compare.py
```
