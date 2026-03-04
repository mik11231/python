#!/usr/bin/env bash
# Architecture Notes:
# - This script is documented so operators can rebuild behavior from comments alone.
# - Structure follows: input acquisition -> normalization -> solving -> reporting.
# - Keep side effects explicit and measured in runtime/benchmark workflows.

set -euo pipefail
EXPECTED_SHA='697301449f3f32ff9e73436c0ee11191f61f63d01afda5637bf644c5aa6042bc'
EXPECTED_PART1='371'
EXPECTED_PART2='369601'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day3/d3_input.txt" "Day3/d3_input.txt" "../Day3/d3_input.txt" "../../Day3/d3_input.txt"; do
    [[ -f "$c" ]] && echo "$c" && return 0
  done
  echo "input not found" >&2; exit 1
}

part=""; input=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --part) part="$2"; shift 2;;
    --input) input="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 1;;
  esac
done
[[ "$part" == "1" || "$part" == "2" ]] || { echo "--part 1|2 required" >&2; exit 1; }
[[ -n "$input" ]] || input="$(default_input)"
got="$(sha256_file "$input")"
[[ "$got" == "$EXPECTED_SHA" ]] || { echo "checksum mismatch" >&2; exit 2; }
start_ns=$(date +%s%N)

ans="$({
  awk -v part="$part" '
    function abs(v) { return v < 0 ? -v : v }
    function key(x, y) { return x "," y }
    function neigh_sum(x, y,    s, dx, dy) {
      s = 0
      for (dx = -1; dx <= 1; dx++) {
        for (dy = -1; dy <= 1; dy++) {
          if (dx == 0 && dy == 0) continue
          s += grid[key(x + dx, y + dy)]
        }
      }
      return s
    }
    {
      gsub(/[[:space:]]/, "", $0)
      n = $0 + 0
      if (part == 1) {
        if (n == 1) { print 0; exit }
        layer = 0
        while (((2 * layer + 1) * (2 * layer + 1)) < n) layer++
        side = 2 * layer
        maxv = (2 * layer + 1) * (2 * layer + 1)
        best = 1e18
        for (i = 0; i < 4; i++) {
          mid = maxv - layer - side * i
          d = abs(n - mid)
          if (d < best) best = d
        }
        print layer + best
        exit
      }

      x = 0; y = 0
      delete grid
      grid[key(0, 0)] = 1
      step = 1
      while (1) {
        for (i = 1; i <= step; i++) {
          x++
          v = neigh_sum(x, y)
          if (v > n) { print v; exit }
          grid[key(x, y)] = v
        }
        for (i = 1; i <= step; i++) {
          y++
          v = neigh_sum(x, y)
          if (v > n) { print v; exit }
          grid[key(x, y)] = v
        }
        step++
        for (i = 1; i <= step; i++) {
          x--
          v = neigh_sum(x, y)
          if (v > n) { print v; exit }
          grid[key(x, y)] = v
        }
        for (i = 1; i <= step; i++) {
          y--
          v = neigh_sum(x, y)
          if (v > n) { print v; exit }
          grid[key(x, y)] = v
        }
        step++
      }
    }
  ' "$input"
})"

if [[ "$part" == "1" ]]; then expected="$EXPECTED_PART1"; else expected="$EXPECTED_PART2"; fi
[[ "$ans" == "$expected" ]] || { echo "answer mismatch: got $ans expected $expected" >&2; exit 3; }

echo "$ans"
end_ns=$(date +%s%N)
elapsed_ns=$((end_ns - start_ns))
ms_int=$((elapsed_ns / 1000000))
ms_frac=$(((elapsed_ns / 1000) % 1000))
ms="$(printf "%d.%03d" "$ms_int" "$ms_frac")"
printf "[bash-fancy] day=%d part=%d runtime_ms=%.3f\n" 3 "$part" "$ms" >&2
