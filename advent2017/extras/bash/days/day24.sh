#!/usr/bin/env bash
set -euo pipefail
EXPECTED_SHA='48a139f917d7dac161171c28f578d923b212c10108c92bbe05a971f6d8b4fb05'
PART1='1656'
PART2='1642'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day24/d24_input.txt" "Day24/d24_input.txt" "../Day24/d24_input.txt" "../../Day24/d24_input.txt"; do
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

declare -a A B
declare -A BY
n=0
while IFS= read -r line || [[ -n "$line" ]]; do
  [[ -n "${line// }" ]] || continue
  a="${line%%/*}"
  b="${line##*/}"
  A[n]="$a"
  B[n]="$b"
  if [[ -n "${BY[$a]:-}" ]]; then BY["$a"]+=",${n}"; else BY["$a"]="$n"; fi
  if [[ "$b" != "$a" ]]; then
    if [[ -n "${BY[$b]:-}" ]]; then BY["$b"]+=",${n}"; else BY["$b"]="$n"; fi
  fi
  n=$((n + 1))
done < "$input"

best_strength=0
best_len=0
best_len_strength=0

dfs() {
  local port="$1"
  local used="$2"
  local length="$3"
  local strength="$4"
  local list ids idx a b nxt seg

  if (( strength > best_strength )); then best_strength="$strength"; fi
  if (( length > best_len || (length == best_len && strength > best_len_strength) )); then
    best_len="$length"
    best_len_strength="$strength"
  fi

  list="${BY[$port]:-}"
  [[ -n "$list" ]] || return
  IFS=',' read -r -a ids <<<"$list"
  for idx in "${ids[@]}"; do
    if (( (used >> idx) & 1 )); then
      continue
    fi
    a="${A[$idx]}"
    b="${B[$idx]}"
    if (( a == port )); then
      nxt="$b"
    else
      nxt="$a"
    fi
    seg=$((a + b))
    dfs "$nxt" "$((used | (1 << idx)))" "$((length + 1))" "$((strength + seg))"
  done
}

dfs 0 0 0 0
if [[ "$part" == "1" ]]; then
  ans="$best_strength"
else
  ans="$best_len_strength"
fi

if [[ "$part" == "1" ]]; then expected="$PART1"; else expected="$PART2"; fi
[[ "$ans" == "$expected" ]] || { echo "answer mismatch: got $ans expected $expected" >&2; exit 3; }
echo "$ans"
end_ns=$(date +%s%N)
elapsed_ns=$((end_ns - start_ns))
ms_int=$((elapsed_ns / 1000000))
ms_frac=$(((elapsed_ns / 1000) % 1000))
printf "[bash-fancy] day=%d part=%d runtime_ms=%d.%03d\n" 24 "$part" "$ms_int" "$ms_frac" >&2
