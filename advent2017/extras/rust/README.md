# Rust X Solver

Native Rust per-day binaries tuned for release performance and strict deterministic execution.

## Architecture

- Each day implementation is isolated in `src/bin/dayNN.rs`.
- Data structures and loops are selected for cache-friendly iteration and minimal allocation churn.
- Build profile favors runtime speed (`lto`, reduced codegen units, abort-on-panic).

## Usage

```bash
cargo build --release
./target/release/aoc2017x --day 24 --part 2 --input ../../Day24/d24_input.txt
./target/release/aoc2017x --all
```
