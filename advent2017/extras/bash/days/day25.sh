#!/usr/bin/env bash
# Architecture Notes:
# - This script is documented so operators can rebuild behavior from comments alone.
# - Structure follows: input acquisition -> normalization -> solving -> reporting.
# - Keep side effects explicit and measured in runtime/benchmark workflows.

set -euo pipefail
EXPECTED_SHA='6419303e9eeb435a39b6e7d17236cb0d3fdfc9b0c2e5d5da8a9864b527c7e873'
PART1='3145'
PART2='Merry Christmas'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day25/d25_input.txt" "Day25/d25_input.txt" "../Day25/d25_input.txt" "../../Day25/d25_input.txt"; do
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

if [[ "$part" == "2" ]]; then
  ans="$PART2"
else
  declare -A W M N
  start_state=""
  steps=0
  cur_state=""
  cur_val=-1
  while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ "$line" =~ ^Begin\ in\ state\ ([A-Z])\. ]]; then
      start_state="${BASH_REMATCH[1]}"
    elif [[ "$line" =~ ^Perform\ a\ diagnostic\ checksum\ after\ ([0-9]+)\ steps\. ]]; then
      steps="${BASH_REMATCH[1]}"
    elif [[ "$line" =~ ^In\ state\ ([A-Z]): ]]; then
      cur_state="${BASH_REMATCH[1]}"
    elif [[ "$line" =~ ^[[:space:]]*If\ the\ current\ value\ is\ ([01]): ]]; then
      cur_val="${BASH_REMATCH[1]}"
    elif [[ "$line" =~ ^[[:space:]]*-\ Write\ the\ value\ ([01])\. ]]; then
      W["$cur_state,$cur_val"]="${BASH_REMATCH[1]}"
    elif [[ "$line" =~ ^[[:space:]]*-\ Move\ one\ slot\ to\ the\ (left|right)\. ]]; then
      if [[ "${BASH_REMATCH[1]}" == "left" ]]; then
        M["$cur_state,$cur_val"]=-1
      else
        M["$cur_state,$cur_val"]=1
      fi
    elif [[ "$line" =~ ^[[:space:]]*-\ Continue\ with\ state\ ([A-Z])\. ]]; then
      N["$cur_state,$cur_val"]="${BASH_REMATCH[1]}"
    fi
  done < "$input"

  declare -A TAPE
  pos=0
  state="$start_state"
  for ((i=0; i<steps; i++)); do
    keyp="$pos"
    cur="${TAPE[$keyp]:-0}"
    key="$state,$cur"
    w="${W[$key]}"
    m="${M[$key]}"
    ns="${N[$key]}"
    if (( w == 1 )); then
      TAPE["$keyp"]=1
    else
      unset 'TAPE[$keyp]'
    fi
    pos=$((pos + m))
    state="$ns"
  done
  ans="${#TAPE[@]}"
fi

if [[ "$part" == "1" ]]; then expected="$PART1"; else expected="$PART2"; fi
[[ "$ans" == "$expected" ]] || { echo "answer mismatch: got $ans expected $expected" >&2; exit 3; }
echo "$ans"
end_ns=$(date +%s%N)
elapsed_ns=$((end_ns - start_ns))
ms_int=$((elapsed_ns / 1000000))
ms_frac=$(((elapsed_ns / 1000) % 1000))
printf "[bash-fancy] day=%d part=%d runtime_ms=%d.%03d\n" 25 "$part" "$ms_int" "$ms_frac" >&2
