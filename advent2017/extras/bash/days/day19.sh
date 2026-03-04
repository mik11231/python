#!/usr/bin/env bash
set -euo pipefail
EXPECTED_SHA='b4231dede8cc9f00c1dcdf6fe60b2c5cc33278020531f4a05af462099063171a'
EXPECTED_PART1='DTOUFARJQ'
EXPECTED_PART2='16642'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day19/d19_input.txt" "Day19/d19_input.txt" "../Day19/d19_input.txt" "../../Day19/d19_input.txt"; do
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

declare -a G
w=0
while IFS= read -r line || [[ -n "$line" ]]; do
  G+=("$line")
  (( ${#line} > w )) && w=${#line}
done < "$input"
h="${#G[@]}"
for ((i=0; i<h; i++)); do
  line="${G[$i]}"
  while (( ${#line} < w )); do line+=" "; done
  G[$i]="$line"
done

at() {
  local rr="$1" cc="$2"
  if (( rr < 0 || rr >= h || cc < 0 || cc >= w )); then
    printf " "
    return
  fi
  printf "%s" "${G[$rr]:$cc:1}"
}

r=0
c=0
while (( c < w )); do
  [[ "${G[0]:$c:1}" == "|" ]] && break
  c=$((c + 1))
done
dr=1
dc=0
letters=""
steps=0
while :; do
  ch="$(at "$r" "$c")"
  [[ "$ch" == " " ]] && break
  if [[ "$ch" =~ [A-Z] ]]; then
    letters+="$ch"
  elif [[ "$ch" == "+" ]]; then
    if (( dr != 0 )); then
      if [[ "$(at "$r" "$((c-1))")" != " " ]]; then
        dr=0; dc=-1
      elif [[ "$(at "$r" "$((c+1))")" != " " ]]; then
        dr=0; dc=1
      fi
    else
      if [[ "$(at "$((r-1))" "$c")" != " " ]]; then
        dr=-1; dc=0
      elif [[ "$(at "$((r+1))" "$c")" != " " ]]; then
        dr=1; dc=0
      fi
    fi
  fi
  r=$((r + dr))
  c=$((c + dc))
  steps=$((steps + 1))
done

if [[ "$part" == "1" ]]; then
  ans="$letters"
else
  ans="$steps"
fi

if [[ "$part" == "1" ]]; then expected="$EXPECTED_PART1"; else expected="$EXPECTED_PART2"; fi
[[ "$ans" == "$expected" ]] || { echo "answer mismatch: got $ans expected $expected" >&2; exit 3; }

echo "$ans"
end_ns=$(date +%s%N)
elapsed_ns=$((end_ns - start_ns))
ms_int=$((elapsed_ns / 1000000))
ms_frac=$(((elapsed_ns / 1000) % 1000))
ms="$(printf "%d.%03d" "$ms_int" "$ms_frac")"
printf "[bash-fancy] day=%d part=%d runtime_ms=%.3f\n" 19 "$part" "$ms" >&2
