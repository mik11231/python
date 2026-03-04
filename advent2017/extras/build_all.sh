#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Native helper binaries for heavy interpreted loops
mkdir -p native/bin
cc -O3 -march=native -mtune=native -fomit-frame-pointer -o native/bin/day15_fast native/day15_fast.c
cc -O3 -march=native -mtune=native -fomit-frame-pointer -o native/bin/day17_fast native/day17_fast.c

# Go per-day binaries
mkdir -p go/bin go/.gocache
for d in $(seq -w 1 25); do
  (cd go && GOCACHE="$PWD/.gocache" go build -o "../go/bin/day$d" "./cmd/day$d")
done

# Rust per-day binaries
(cd rust && cargo build --release --bins)

# C++ per-day binaries
(cd cxx && cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j)

echo "Build complete"
