#!/usr/bin/env bash
# Architecture Notes:
# - This script is documented so operators can rebuild behavior from comments alone.
# - Structure follows: input acquisition -> normalization -> solving -> reporting.
# - Keep side effects explicit and measured in runtime/benchmark workflows.

set -euo pipefail
EXPECTED_SHA='8d4f35b1950c1ca0bd04c13fe9e4a9a15065f902a86a82606973db0b9fe346f7'
EXPECTED_PART1='650'
EXPECTED_PART2='336'
FA=16807
FB=48271
MOD=2147483647
MASK=65535

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day15/d15_input.txt" "Day15/d15_input.txt" "../Day15/d15_input.txt" "../../Day15/d15_input.txt"; do
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

a_seed=0
b_seed=0
line_no=0
while IFS= read -r line || [[ -n "$line" ]]; do
  [[ -n "${line// }" ]] || continue
  line_no=$((line_no + 1))
  val="${line##* }"
  if (( line_no == 1 )); then a_seed="$val"; fi
  if (( line_no == 2 )); then b_seed="$val"; fi
done < "$input"

a="$a_seed"
b="$b_seed"
cnt=0
if [[ "$part" == "1" ]]; then
  for ((i=0; i<40000000; i++)); do
    a=$(( (a * FA) % MOD ))
    b=$(( (b * FB) % MOD ))
    if (( (a & MASK) == (b & MASK) )); then
      cnt=$((cnt + 1))
    fi
  done
else
  for ((i=0; i<5000000; i++)); do
    while :; do
      a=$(( (a * FA) % MOD ))
      (( (a & 3) == 0 )) && break
    done
    while :; do
      b=$(( (b * FB) % MOD ))
      (( (b & 7) == 0 )) && break
    done
    if (( (a & MASK) == (b & MASK) )); then
      cnt=$((cnt + 1))
    fi
  done
fi
ans="$cnt"

if [[ "$part" == "1" ]]; then expected="$EXPECTED_PART1"; else expected="$EXPECTED_PART2"; fi
[[ "$ans" == "$expected" ]] || { echo "answer mismatch: got $ans expected $expected" >&2; exit 3; }

echo "$ans"
end_ns=$(date +%s%N)
elapsed_ns=$((end_ns - start_ns))
ms_int=$((elapsed_ns / 1000000))
ms_frac=$(((elapsed_ns / 1000) % 1000))
printf "[bash-fancy] day=%d part=%d runtime_ms=%d.%03d\n" 15 "$part" "$ms_int" "$ms_frac" >&2
