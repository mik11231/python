#!/usr/bin/env bash
# Architecture Notes:
# - This script is documented so operators can rebuild behavior from comments alone.
# - Structure follows: input acquisition -> normalization -> solving -> reporting.
# - Keep side effects explicit and measured in runtime/benchmark workflows.

set -euo pipefail
EXPECTED_SHA='b83c8a7c9fb42d39b4545428717df7858882f3644a62d2770c235c9eb61ace69'
EXPECTED_PART1='54675'
EXPECTED_PART2='a7af2706aa9a09cf5d848c1e6605dd2a'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day10/d10_input.txt" "Day10/d10_input.txt" "../Day10/d10_input.txt" "../../Day10/d10_input.txt"; do
    [[ -f "$c" ]] && echo "$c" && return 0
  done
  echo "input not found" >&2; exit 1
}

reverse_segment() {
  local start=$1 len=$2 n=${#ring[@]}
  local i x y tmp
  for ((i=0; i<len/2; i++)); do
    x=$(((start + i) % n))
    y=$(((start + len - 1 - i) % n))
    tmp=${ring[x]}
    ring[x]=${ring[y]}
    ring[y]=$tmp
  done
}

run_round() {
  local -n lens_ref=$1
  local n=${#ring[@]}
  local len
  for len in "${lens_ref[@]}"; do
    reverse_segment "$pos" "$len"
    pos=$(((pos + len + skip) % n))
    skip=$((skip + 1))
  done
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

raw="$(tr -d '\r\n' < "$input")"
declare -a ring
for ((i=0; i<256; i++)); do ring[i]=$i; done
pos=0
skip=0

if [[ "$part" == "1" ]]; then
  IFS=',' read -r -a lengths <<< "$raw"
  run_round lengths
  ans=$(( ring[0] * ring[1] ))
else
  declare -a lengths=()
  for ((i=0; i<${#raw}; i++)); do
    ch=${raw:i:1}
    lengths+=("$(printf '%d' "'$ch")")
  done
  lengths+=(17 31 73 47 23)

  for ((round=0; round<64; round++)); do
    run_round lengths
  done

  ans=""
  for ((block=0; block<16; block++)); do
    x=0
    for ((j=0; j<16; j++)); do
      idx=$((block*16 + j))
      x=$((x ^ ring[idx]))
    done
    printf -v hx "%02x" "$x"
    ans+="$hx"
  done
fi

if [[ "$part" == "1" ]]; then expected="$EXPECTED_PART1"; else expected="$EXPECTED_PART2"; fi
[[ "$ans" == "$expected" ]] || { echo "answer mismatch: got $ans expected $expected" >&2; exit 3; }

echo "$ans"
end_ns=$(date +%s%N)
elapsed_ns=$((end_ns - start_ns))
ms_int=$((elapsed_ns / 1000000))
ms_frac=$(((elapsed_ns / 1000) % 1000))
ms="$(printf "%d.%03d" "$ms_int" "$ms_frac")"
printf "[bash-fancy] day=%d part=%d runtime_ms=%.3f\n" 10 "$part" "$ms" >&2
