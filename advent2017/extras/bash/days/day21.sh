#!/usr/bin/env bash
# Architecture Notes:
# - This script is documented so operators can rebuild behavior from comments alone.
# - Structure follows: input acquisition -> normalization -> solving -> reporting.
# - Keep side effects explicit and measured in runtime/benchmark workflows.

set -euo pipefail
EXPECTED_SHA='759a25acf919be68478e4d20d3856f488ff79325d0954d8ca5c89cecc2fd8287'
PART1='139'
PART2='1857134'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day21/d21_input.txt" "Day21/d21_input.txt" "../Day21/d21_input.txt" "../../Day21/d21_input.txt"; do
    [[ -f "$c" ]] && echo "$c" && return 0
  done
  echo "input not found" >&2; exit 1
}

pat_rotate() {
  local p="$1"
  local -a r out
  local n i j row
  IFS='/' read -r -a r <<<"$p"
  n="${#r[@]}"
  for ((i=0; i<n; i++)); do
    row=""
    for ((j=0; j<n; j++)); do
      row+="${r[n-1-j]:i:1}"
    done
    out[i]="$row"
  done
  (IFS='/'; echo "${out[*]}")
}

str_rev() {
  local s="$1"
  local out=""
  local i
  for ((i=${#s}-1; i>=0; i--)); do
    out+="${s:i:1}"
  done
  echo "$out"
}

pat_flip() {
  local p="$1"
  local -a r out
  local i
  IFS='/' read -r -a r <<<"$p"
  for ((i=0; i<${#r[@]}; i++)); do
    out[i]="$(str_rev "${r[i]}")"
  done
  (IFS='/'; echo "${out[*]}")
}

pat_canon() {
  local p="$1"
  local cur="$p" f best v
  local i
  best=""
  for ((i=0; i<4; i++)); do
    v="$cur"
    if [[ -z "$best" || "$v" < "$best" ]]; then best="$v"; fi
    f="$(pat_flip "$cur")"
    if [[ "$f" < "$best" ]]; then best="$f"; fi
    cur="$(pat_rotate "$cur")"
  done
  echo "$best"
}

count_hashes_pat() {
  local p="$1"
  local i c=0
  for ((i=0; i<${#p}; i++)); do
    [[ "${p:i:1}" == "#" ]] && c=$((c + 1))
  done
  echo "$c"
}

declare -A RULE
enhance_once() {
  local p="$1"
  local -a g out src_rows dst_rows
  local n k blocks outb br bc i rr cc src dst idx
  IFS='/' read -r -a g <<<"$p"
  n="${#g[@]}"
  if (( n % 2 == 0 )); then k=2; else k=3; fi
  blocks=$((n / k))
  outb=$((k + 1))
  for ((i=0; i<blocks*outb; i++)); do out[i]=""; done

  for ((br=0; br<blocks; br++)); do
    for ((bc=0; bc<blocks; bc++)); do
      for ((i=0; i<k; i++)); do
        src_rows[i]="${g[br*k + i]:bc*k:k}"
      done
      local IFS='/'
      src="${src_rows[*]}"
      dst="${RULE[$(pat_canon "$src")]}"
      IFS='/' read -r -a dst_rows <<<"$dst"
      for ((i=0; i<outb; i++)); do
        idx=$((br*outb + i))
        out[idx]+="${dst_rows[i]}"
      done
    done
  done
  (IFS='/'; echo "${out[*]}")
}

declare -A EXPAND3
expand3_get() {
  local p="$1"
  local g bkey
  local -a rows blocks
  local br bc i
  if [[ -n "${EXPAND3[$p]:-}" ]]; then
    echo "${EXPAND3[$p]}"
    return
  fi
  g="$p"
  g="$(enhance_once "$g")"
  g="$(enhance_once "$g")"
  g="$(enhance_once "$g")"
  IFS='/' read -r -a rows <<<"$g"
  blocks=()
  for ((br=0; br<3; br++)); do
    for ((bc=0; bc<3; bc++)); do
      r0=$((br * 3))
      r1=$((r0 + 1))
      r2=$((r0 + 2))
      c0=$((bc * 3))
      bkey="${rows[$r0]:$c0:3}/${rows[$r1]:$c0:3}/${rows[$r2]:$c0:3}"
      blocks+=("$bkey")
    done
  done
  local IFS='|'
  EXPAND3["$p"]="${blocks[*]}"
  echo "${EXPAND3[$p]}"
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

while IFS= read -r line || [[ -n "$line" ]]; do
  [[ -n "${line// }" ]] || continue
  left="${line%% => *}"
  right="${line##* => }"
  RULE["$(pat_canon "$left")"]="$right"
done < "$input"

start_pat=".#./..#/###"
if [[ "$part" == "1" ]]; then
  g="$start_pat"
  for ((i=0; i<5; i++)); do
    g="$(enhance_once "$g")"
  done
  ans="$(count_hashes_pat "$g")"
else
  declare -A CUR NXT
  CUR["$start_pat"]=1
  for ((cycle=0; cycle<6; cycle++)); do
    NXT=()
    for pat in "${!CUR[@]}"; do
      cnt="${CUR[$pat]}"
      exp="$(expand3_get "$pat")"
      IFS='|' read -r -a blocks <<<"$exp"
      for b in "${blocks[@]}"; do
        NXT["$b"]=$(( ${NXT[$b]:-0} + cnt ))
      done
    done
    CUR=()
    for pat in "${!NXT[@]}"; do CUR["$pat"]="${NXT[$pat]}"; done
  done
  total=0
  for pat in "${!CUR[@]}"; do
    h="$(count_hashes_pat "$pat")"
    total=$((total + h * CUR[$pat]))
  done
  ans="$total"
fi

if [[ "$part" == "1" ]]; then expected="$PART1"; else expected="$PART2"; fi
[[ "$ans" == "$expected" ]] || { echo "answer mismatch: got $ans expected $expected" >&2; exit 3; }
echo "$ans"
end_ns=$(date +%s%N)
elapsed_ns=$((end_ns - start_ns))
ms_int=$((elapsed_ns / 1000000))
ms_frac=$(((elapsed_ns / 1000) % 1000))
printf "[bash-fancy] day=%d part=%d runtime_ms=%d.%03d\n" 21 "$part" "$ms_int" "$ms_frac" >&2
