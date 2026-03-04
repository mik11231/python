# C++ X Solver

Native C++ per-day binaries using aggressive optimization flags and explicit low-level control.

## Architecture

- Day units live in `src/days/dayNN.cpp` and compile into optimized release executables.
- Implementations prioritize tight loops, compact data representations, and predictable branches.
- Runtime telemetry integrates with repository benchmark tooling.

## Usage

```bash
cmake -S . -B build
cmake --build build -j
./build/aoc2017x --day 24 --part 2 --input ../../Day24/d24_input.txt
./build/aoc2017x --all
```
