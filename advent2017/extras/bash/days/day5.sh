#!/usr/bin/env bash
# Architecture Notes:
# - This script is documented so operators can rebuild behavior from comments alone.
# - Structure follows: input acquisition -> normalization -> solving -> reporting.
# - Keep side effects explicit and measured in runtime/benchmark workflows.

set -euo pipefail
EXPECTED_SHA='e9c74e01657b99ad1be3cedce52f75bb0e2ac9dfb2efca8714f5f2e0910befa6'
EXPECTED_PART1='394829'
EXPECTED_PART2='31150702'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day5/d5_input.txt" "Day5/d5_input.txt" "../Day5/d5_input.txt" "../../Day5/d5_input.txt"; do
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

# Jump-offset VM simulation in awk. Part 1 always increments current offset,
# while Part 2 decrements when current offset >= 3.
ans="$({
  awk -v part="$part" '
    { a[n++] = int($1) }
    END {
      i = 0
      steps = 0
      while (i >= 0 && i < n) {
        jump = a[i]
        if (part == 1) {
          a[i] = jump + 1
        } else {
          if (jump >= 3) a[i] = jump - 1
          else a[i] = jump + 1
        }
        i += jump
        steps++
      }
      print steps
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
printf "[bash-fancy] day=%d part=%d runtime_ms=%.3f\n" 5 "$part" "$ms" >&2
