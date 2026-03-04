#!/usr/bin/env bash
# Architecture Notes:
# - This script is documented so operators can rebuild behavior from comments alone.
# - Structure follows: input acquisition -> normalization -> solving -> reporting.
# - Keep side effects explicit and measured in runtime/benchmark workflows.

set -euo pipefail
EXPECTED_SHA='03a3d955b8799a90f1ff5a39479fde8e618f8ca3282d5b187186f2cf361abd32'
EXPECTED_PART1='808'
EXPECTED_PART2='47465686'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day17/d17_input.txt" "Day17/d17_input.txt" "../Day17/d17_input.txt" "../../Day17/d17_input.txt"; do
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

step="$(tr -d '\r\n' < "$input")"
if [[ "$part" == "1" ]]; then
  declare -a buf
  buf=(0)
  size=1
  pos=0
  for ((v=1; v<=2017; v++)); do
    pos=$(( ((pos + step) % size) + 1 ))
    for ((j=size; j>pos; j--)); do
      buf[j]="${buf[j-1]}"
    done
    buf[pos]="$v"
    size=$((size + 1))
  done
  ans="${buf[$(((pos + 1) % size))]}"
else
  pos=0
  size=1
  after0=0
  for ((v=1; v<=50000000; v++)); do
    pos=$(( ((pos + step) % size) + 1 ))
    if (( pos == 1 )); then
      after0="$v"
    fi
    size=$((size + 1))
  done
  ans="$after0"
fi

if [[ "$part" == "1" ]]; then expected="$EXPECTED_PART1"; else expected="$EXPECTED_PART2"; fi
[[ "$ans" == "$expected" ]] || { echo "answer mismatch: got $ans expected $expected" >&2; exit 3; }

echo "$ans"
end_ns=$(date +%s%N)
elapsed_ns=$((end_ns - start_ns))
ms_int=$((elapsed_ns / 1000000))
ms_frac=$(((elapsed_ns / 1000) % 1000))
printf "[bash-fancy] day=%d part=%d runtime_ms=%d.%03d\n" 17 "$part" "$ms_int" "$ms_frac" >&2
