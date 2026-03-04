#!/usr/bin/env bash
set -euo pipefail
EXPECTED_SHA='489246369534515a9df814e8824f41c427d6c02ab31d7b5c07cbdc935497f2ba'
EXPECTED_PART1='12841'
EXPECTED_PART2='8038'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day6/d6_input.txt" "Day6/d6_input.txt" "../Day6/d6_input.txt" "../../Day6/d6_input.txt"; do
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
    function state_key(    i, k) {
      k = banks[0]
      for (i = 1; i < n; i++) k = k "," banks[i]
      return k
    }
    function redistribute(    i, k, blocks, q, r, idx) {
      idx = 0
      for (i = 1; i < n; i++) {
        if (banks[i] > banks[idx]) idx = i
      }
      blocks = banks[idx]
      banks[idx] = 0
      q = int(blocks / n)
      r = blocks % n
      if (q > 0) {
        for (i = 0; i < n; i++) banks[i] += q
      }
      for (k = 1; k <= r; k++) {
        banks[(idx + k) % n]++
      }
    }
    {
      for (i = 1; i <= NF; i++) banks[n++] = int($i)
    }
    END {
      steps = 0
      while (1) {
        key = state_key()
        if (key in seen) {
          if (part == 1) print steps
          else print steps - seen[key]
          exit
        }
        seen[key] = steps
        redistribute()
        steps++
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
printf "[bash-fancy] day=%d part=%d runtime_ms=%.3f\n" 6 "$part" "$ms" >&2
