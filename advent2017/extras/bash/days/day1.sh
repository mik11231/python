#!/usr/bin/env bash
set -euo pipefail
EXPECTED_SHA='ffefe22d570c7077ac45df89cd8a40c99990e1903f6e68a501d75e53038c80ef'
EXPECTED_PART1='1158'
EXPECTED_PART2='1132'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day1/d1_input.txt" "Day1/d1_input.txt" "../Day1/d1_input.txt" "../../Day1/d1_input.txt"; do
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

# Real AoC Day 1 algorithm in awk:
# part 1 => compare with next digit
# part 2 => compare with halfway-around digit
ans="$(
  awk -v part="$part" '
    {
      gsub(/[[:space:]]/, "", $0)
      s = $0
      n = length(s)
      if (n == 0) { print 0; exit }
      step = (part == 1 ? 1 : int(n / 2))
      sum = 0
      for (i = 1; i <= n; i++) {
        c = substr(s, i, 1)
        j = ((i - 1 + step) % n) + 1
        if (c == substr(s, j, 1)) sum += c + 0
      }
      print sum
      exit
    }
  ' "$input"
)"

if [[ "$part" == "1" ]]; then
  expected="$EXPECTED_PART1"
else
  expected="$EXPECTED_PART2"
fi
[[ "$ans" == "$expected" ]] || { echo "answer mismatch: got $ans expected $expected" >&2; exit 3; }

echo "$ans"
end_ns=$(date +%s%N)
elapsed_ns=$((end_ns - start_ns))
ms_int=$((elapsed_ns / 1000000))
ms_frac=$(((elapsed_ns / 1000) % 1000))
ms="$(printf "%d.%03d" "$ms_int" "$ms_frac")"
printf "[bash-fancy] day=%d part=%d runtime_ms=%.3f\n" 1 "$part" "$ms" >&2
