#!/usr/bin/env bash
set -euo pipefail
EXPECTED_SHA='9480ad6f4d423780a0542e172e614170ec28d3eb06c80b7c2b452c6ceeecbfb0'
PART1='144'
PART2='477'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day20/d20_input.txt" "Day20/d20_input.txt" "../Day20/d20_input.txt" "../../Day20/d20_input.txt"; do
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

declare -a PX PY PZ VX VY VZ AX AY AZ ALIVE
n=0
while IFS= read -r line || [[ -n "$line" ]]; do
  [[ -n "${line// }" ]] || continue
  clean="${line//[^0-9-]/ }"
  read -r -a vals <<<"$clean"
  PX[n]="${vals[0]}"; PY[n]="${vals[1]}"; PZ[n]="${vals[2]}"
  VX[n]="${vals[3]}"; VY[n]="${vals[4]}"; VZ[n]="${vals[5]}"
  AX[n]="${vals[6]}"; AY[n]="${vals[7]}"; AZ[n]="${vals[8]}"
  ALIVE[n]=1
  n=$((n + 1))
done < "$input"

if [[ "$part" == "1" ]]; then
  best_i=-1
  best_a=0
  best_v=0
  best_p=0
  for ((i=0; i<n; i++)); do
    a=$(( ${AX[i]#-} + ${AY[i]#-} + ${AZ[i]#-} ))
    v=$(( ${VX[i]#-} + ${VY[i]#-} + ${VZ[i]#-} ))
    p=$(( ${PX[i]#-} + ${PY[i]#-} + ${PZ[i]#-} ))
    if (( best_i < 0 || a < best_a || (a == best_a && (v < best_v || (v == best_v && (p < best_p || (p == best_p && i < best_i)))) ) )); then
      best_i="$i"
      best_a="$a"
      best_v="$v"
      best_p="$p"
    fi
  done
  ans="$best_i"
else
  for ((t=0; t<200; t++)); do
    declare -A POS_COUNT
    declare -a POS_KEY
    for ((i=0; i<n; i++)); do
      (( ALIVE[i] == 1 )) || continue
      VX[i]=$((VX[i] + AX[i]))
      VY[i]=$((VY[i] + AY[i]))
      VZ[i]=$((VZ[i] + AZ[i]))
      PX[i]=$((PX[i] + VX[i]))
      PY[i]=$((PY[i] + VY[i]))
      PZ[i]=$((PZ[i] + VZ[i]))
      key="${PX[i]},${PY[i]},${PZ[i]}"
      POS_KEY[$i]="$key"
      POS_COUNT["$key"]=$(( ${POS_COUNT[$key]:-0} + 1 ))
    done
    for ((i=0; i<n; i++)); do
      (( ALIVE[i] == 1 )) || continue
      key="${POS_KEY[$i]}"
      if (( ${POS_COUNT[$key]:-0} > 1 )); then
        ALIVE[i]=0
      fi
    done
  done
  alive_cnt=0
  for ((i=0; i<n; i++)); do
    (( ALIVE[i] == 1 )) && alive_cnt=$((alive_cnt + 1))
  done
  ans="$alive_cnt"
fi

if [[ "$part" == "1" ]]; then expected="$PART1"; else expected="$PART2"; fi
[[ "$ans" == "$expected" ]] || { echo "answer mismatch: got $ans expected $expected" >&2; exit 3; }
echo "$ans"
end_ns=$(date +%s%N)
elapsed_ns=$((end_ns - start_ns))
ms_int=$((elapsed_ns / 1000000))
ms_frac=$(((elapsed_ns / 1000) % 1000))
printf "[bash-fancy] day=%d part=%d runtime_ms=%d.%03d\n" 20 "$part" "$ms_int" "$ms_frac" >&2
