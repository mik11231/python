#!/usr/bin/env bash
# Architecture Notes:
# - This script is documented so operators can rebuild behavior from comments alone.
# - Structure follows: input acquisition -> normalization -> solving -> reporting.
# - Keep side effects explicit and measured in runtime/benchmark workflows.

set -euo pipefail
EXPECTED_SHA='860cd63e00136c29310e25db6f4f1573a2b2574598dc72f44a6308ddf5a967c3'
EXPECTED_PART1='21037'
EXPECTED_PART2='9495'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day9/d9_input.txt" "Day9/d9_input.txt" "../Day9/d9_input.txt" "../../Day9/d9_input.txt"; do
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
    {
      gsub(/[[:space:]]/, "", $0)
      s = $0
      depth = 0
      score = 0
      garb = 0
      cnt = 0
      i = 1
      while (i <= length(s)) {
        c = substr(s, i, 1)
        if (garb) {
          if (c == "!") { i += 2; continue }
          if (c == ">") garb = 0
          else cnt++
        } else {
          if (c == "<") garb = 1
          else if (c == "{") { depth++; score += depth }
          else if (c == "}") depth--
        }
        i++
      }
      if (part == 1) print score
      else print cnt
      exit
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
printf "[bash-fancy] day=%d part=%d runtime_ms=%.3f\n" 9 "$part" "$ms" >&2
