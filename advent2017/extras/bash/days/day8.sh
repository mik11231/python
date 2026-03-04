#!/usr/bin/env bash
# Architecture Notes:
# - This script is documented so operators can rebuild behavior from comments alone.
# - Structure follows: input acquisition -> normalization -> solving -> reporting.
# - Keep side effects explicit and measured in runtime/benchmark workflows.

set -euo pipefail
EXPECTED_SHA='a2888c695f7f2c036f5d9568befc839a3b64c703d054f82162cfbc5e105627dd'
EXPECTED_PART1='5143'
EXPECTED_PART2='6209'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day8/d8_input.txt" "Day8/d8_input.txt" "../Day8/d8_input.txt" "../../Day8/d8_input.txt"; do
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
    function cond(a, op, b) {
      if (op == "<") return a < b
      if (op == "<=") return a <= b
      if (op == ">") return a > b
      if (op == ">=") return a >= b
      if (op == "==") return a == b
      return a != b
    }
    {
      r = $1; op = $2; v = $3 + 0; cr = $5; cmpop = $6; cv = $7 + 0
      if (cond(reg[cr], cmpop, cv)) {
        if (op == "inc") reg[r] += v
        else reg[r] -= v
        if (reg[r] > best) best = reg[r]
      }
    }
    END {
      maxv = 0
      first = 1
      for (k in reg) {
        if (first || reg[k] > maxv) { maxv = reg[k]; first = 0 }
      }
      if (part == 1) print maxv
      else print best
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
printf "[bash-fancy] day=%d part=%d runtime_ms=%.3f\n" 8 "$part" "$ms" >&2
