#!/usr/bin/env bash
set -euo pipefail
EXPECTED_SHA='6bb64ef97ccf665f21eccff0a7045717f0a03d39ae06aaac5495dd6fff650818'
EXPECTED_PART1='kgdchlfniambejop'
EXPECTED_PART2='fjpmholcibdgeakn'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day16/d16_input.txt" "Day16/d16_input.txt" "../Day16/d16_input.txt" "../../Day16/d16_input.txt"; do
    [[ -f "$c" ]] && echo "$c" && return 0
  done
  echo "input not found" >&2; exit 1
}

to_idx() { printf "%d" "$(( $(printf '%d' "'$1") - 97 ))"; }
to_chr() { printf "\\$(printf '%03o' "$((97 + $1))")"; }

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
IFS=',' read -r -a moves <<<"$raw"

# Build one-round position source map and name map.
declare -a pos_arr name_map
for ((i=0; i<16; i++)); do
  pos_arr[i]="$i"
  name_map[i]="$i"
done

for mv in "${moves[@]}"; do
  t="${mv:0:1}"
  arg="${mv:1}"
  if [[ "$t" == "s" ]]; then
    x="$arg"
    declare -a tmp
    for ((j=0; j<16; j++)); do
      src=$(((j - x + 16) % 16))
      tmp[j]="${pos_arr[src]}"
    done
    pos_arr=("${tmp[@]}")
  elif [[ "$t" == "x" ]]; then
    a="${arg%%/*}"
    b="${arg##*/}"
    tmp="${pos_arr[a]}"
    pos_arr[a]="${pos_arr[b]}"
    pos_arr[b]="$tmp"
  else
    a="$(to_idx "${arg%%/*}")"
    b="$(to_idx "${arg##*/}")"
    for ((k=0; k<16; k++)); do
      if (( name_map[k] == a )); then
        name_map[k]="$b"
      elif (( name_map[k] == b )); then
        name_map[k]="$a"
      fi
    done
  fi
done

rounds=1
[[ "$part" == "2" ]] && rounds=1000000000

# Binary exponentiation for position map c[j] = p[q[j]] composition.
declare -a pos_base pos_res
pos_base=("${pos_arr[@]}")
for ((i=0; i<16; i++)); do pos_res[i]="$i"; done
r="$rounds"
while (( r > 0 )); do
  if (( r & 1 )); then
    declare -a comb
    for ((j=0; j<16; j++)); do comb[j]="${pos_res[${pos_base[j]}]}"; done
    pos_res=("${comb[@]}")
  fi
  declare -a sq
  for ((j=0; j<16; j++)); do sq[j]="${pos_base[${pos_base[j]}]}"; done
  pos_base=("${sq[@]}")
  r=$((r >> 1))
done

# Binary exponentiation for name map h[x] = g[f[x]].
declare -a name_base name_res
name_base=("${name_map[@]}")
for ((i=0; i<16; i++)); do name_res[i]="$i"; done
r="$rounds"
while (( r > 0 )); do
  if (( r & 1 )); then
    declare -a comb
    for ((j=0; j<16; j++)); do comb[j]="${name_base[${name_res[j]}]}"; done
    name_res=("${comb[@]}")
  fi
  declare -a sq
  for ((j=0; j<16; j++)); do sq[j]="${name_base[${name_base[j]}]}"; done
  name_base=("${sq[@]}")
  r=$((r >> 1))
done

ans=""
for ((j=0; j<16; j++)); do
  lbl="${name_res[${pos_res[j]}]}"
  ans+="$(to_chr "$lbl")"
done

if [[ "$part" == "1" ]]; then expected="$EXPECTED_PART1"; else expected="$EXPECTED_PART2"; fi
[[ "$ans" == "$expected" ]] || { echo "answer mismatch: got $ans expected $expected" >&2; exit 3; }

echo "$ans"
end_ns=$(date +%s%N)
elapsed_ns=$((end_ns - start_ns))
ms_int=$((elapsed_ns / 1000000))
ms_frac=$(((elapsed_ns / 1000) % 1000))
ms="$(printf "%d.%03d" "$ms_int" "$ms_frac")"
printf "[bash-fancy] day=%d part=%d runtime_ms=%.3f\n" 16 "$part" "$ms" >&2
