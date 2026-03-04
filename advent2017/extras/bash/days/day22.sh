#!/usr/bin/env bash
set -euo pipefail
EXPECTED_SHA='29581d7567b692271626cc1b3e1448f3456036af5d0bb1e0714fbaf2cf7bc878'
EXPECTED_PART1='5246'
EXPECTED_PART2='2512059'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day22/d22_input.txt" "Day22/d22_input.txt" "../Day22/d22_input.txt" "../../Day22/d22_input.txt"; do
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

declare -A STATE
declare -a LINES
while IFS= read -r line || [[ -n "$line" ]]; do
  [[ -n "${line// }" ]] || continue
  LINES+=("$line")
done < "$input"
n="${#LINES[@]}"
off=$((n / 2))
for ((r=0; r<n; r++)); do
  row="${LINES[$r]}"
  for ((c=0; c<${#row}; c++)); do
    if [[ "${row:c:1}" == "#" ]]; then
      key="$((r - off)),$((c - off))"
      STATE["$key"]=2
    fi
  done
done

x=0
y=0
d=0
ans=0
if [[ "$part" == "1" ]]; then
  bursts=10000
else
  bursts=10000000
fi

for ((i=0; i<bursts; i++)); do
  key="$x,$y"
  cur="${STATE[$key]:-0}"
  if [[ "$part" == "1" ]]; then
    if (( cur == 2 )); then
      d=$(((d + 1) & 3))
      unset 'STATE[$key]'
    else
      d=$(((d + 3) & 3))
      STATE["$key"]=2
      ans=$((ans + 1))
    fi
  else
    if (( cur == 0 )); then
      d=$(((d + 3) & 3))
      STATE["$key"]=1
    elif (( cur == 1 )); then
      STATE["$key"]=2
      ans=$((ans + 1))
    elif (( cur == 2 )); then
      d=$(((d + 1) & 3))
      STATE["$key"]=3
    else
      d=$(((d + 2) & 3))
      unset 'STATE[$key]'
    fi
  fi

  if (( d == 0 )); then
    x=$((x - 1))
  elif (( d == 1 )); then
    y=$((y + 1))
  elif (( d == 2 )); then
    x=$((x + 1))
  else
    y=$((y - 1))
  fi
done

if [[ "$part" == "1" ]]; then expected="$EXPECTED_PART1"; else expected="$EXPECTED_PART2"; fi
[[ "$ans" == "$expected" ]] || { echo "answer mismatch: got $ans expected $expected" >&2; exit 3; }

echo "$ans"
end_ns=$(date +%s%N)
elapsed_ns=$((end_ns - start_ns))
ms_int=$((elapsed_ns / 1000000))
ms_frac=$(((elapsed_ns / 1000) % 1000))
printf "[bash-fancy] day=%d part=%d runtime_ms=%d.%03d\n" 22 "$part" "$ms_int" "$ms_frac" >&2
