#!/usr/bin/env bash
# Architecture Notes:
# - This script is documented so operators can rebuild behavior from comments alone.
# - Structure follows: input acquisition -> normalization -> solving -> reporting.
# - Keep side effects explicit and measured in runtime/benchmark workflows.

set -euo pipefail
EXPECTED_SHA='866b77a4b5e37e19219792c97103a17d24c5f15a9f0bed448c0e6cfd75378beb'
PART1='3969'
PART2='917'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day23/d23_input.txt" "Day23/d23_input.txt" "../Day23/d23_input.txt" "../../Day23/d23_input.txt"; do
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
declare -a OP XR YR
while IFS= read -r line || [[ -n "$line" ]]; do
  [[ -n "${line// }" ]] || continue
  read -r op x y <<<"$line"
  OP+=("$op")
  XR+=("$x")
  YR+=("${y:-0}")
done < "$input"
n="${#OP[@]}"

is_int() {
  [[ "$1" =~ ^-?[0-9]+$ ]]
}

declare -A REG
get_val() {
  local t="$1"
  if is_int "$t"; then
    echo "$t"
  else
    echo "${REG[$t]:-0}"
  fi
}

is_prime() {
  local n="$1"
  if (( n < 2 )); then return 1; fi
  if (( n % 2 == 0 )); then (( n == 2 )); return $?; fi
  local d=3
  while (( d * d <= n )); do
    if (( n % d == 0 )); then return 1; fi
    d=$((d + 2))
  done
  return 0
}

if [[ "$part" == "1" ]]; then
  ip=0
  muls=0
  while (( ip >= 0 && ip < n )); do
    op="${OP[$ip]}"
    x="${XR[$ip]}"
    y="${YR[$ip]}"
    case "$op" in
      set)
        REG["$x"]="$(get_val "$y")"
        ;;
      sub)
        xv="${REG[$x]:-0}"
        yv="$(get_val "$y")"
        REG["$x"]=$((xv - yv))
        ;;
      mul)
        xv="${REG[$x]:-0}"
        yv="$(get_val "$y")"
        REG["$x"]=$((xv * yv))
        muls=$((muls + 1))
        ;;
      jnz)
        xv="$(get_val "$x")"
        if (( xv != 0 )); then
          yv="$(get_val "$y")"
          ip=$((ip + yv))
          continue
        fi
        ;;
    esac
    ip=$((ip + 1))
  done
  ans="$muls"
else
  b0="${YR[0]}"
  b=$((b0 * 100 + 100000))
  c=$((b + 17000))
  cnt=0
  for ((x=b; x<=c; x+=17)); do
    if ! is_prime "$x"; then
      cnt=$((cnt + 1))
    fi
  done
  ans="$cnt"
fi
if [[ "$part" == "1" ]]; then expected="$PART1"; else expected="$PART2"; fi
[[ "$ans" == "$expected" ]] || { echo "answer mismatch: got $ans expected $expected" >&2; exit 3; }
echo "$ans"
end_ns=$(date +%s%N)
elapsed_ns=$((end_ns - start_ns))
ms_int=$((elapsed_ns / 1000000))
ms_frac=$(((elapsed_ns / 1000) % 1000))
ms="$(printf "%d.%03d" "$ms_int" "$ms_frac")"
printf "[bash-fancy] day=%d part=%d runtime_ms=%.3f\n" 23 "$part" "$ms" >&2
