#!/usr/bin/env bash
# Architecture Notes:
# - This script is documented so operators can rebuild behavior from comments alone.
# - Structure follows: input acquisition -> normalization -> solving -> reporting.
# - Keep side effects explicit and measured in runtime/benchmark workflows.

set -euo pipefail
EXPECTED_SHA='354ac7a7409ec19ac2561c95f08ba4d0df1a26cdda409bef5ba594cff685eb0a'
EXPECTED_PART1='8074'
EXPECTED_PART2='1212'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day14/d14_input.txt" "Day14/d14_input.txt" "../Day14/d14_input.txt" "../../Day14/d14_input.txt"; do
    [[ -f "$c" ]] && echo "$c" && return 0
  done
  echo "input not found" >&2; exit 1
}

popcount8() {
  local x="$1"
  local c=0
  while (( x > 0 )); do
    x=$((x & (x - 1)))
    c=$((c + 1))
  done
  echo "$c"
}

knot_row() {
  local key="$1"
  local -a lengths ring
  local i j round pos skip len n a b t byte bit x row
  for ((i=0; i<256; i++)); do ring[i]="$i"; done
  for ((i=0; i<${#key}; i++)); do
    ch="${key:i:1}"
    printf -v ord "%d" "'$ch"
    lengths+=("$ord")
  done
  lengths+=(17 31 73 47 23)
  pos=0
  skip=0
  n=256
  for ((round=0; round<64; round++)); do
    for len in "${lengths[@]}"; do
      for ((i=0; i<len/2; i++)); do
        a=$(((pos + i) % n))
        b=$(((pos + len - 1 - i) % n))
        t="${ring[$a]}"
        ring[$a]="${ring[$b]}"
        ring[$b]="$t"
      done
      pos=$(((pos + len + skip) % n))
      skip=$((skip + 1))
    done
  done

  row=""
  row_used=0
  for ((i=0; i<16; i++)); do
    x=0
    for ((j=0; j<16; j++)); do
      x=$((x ^ ring[i*16 + j]))
    done
    row_used=$((row_used + $(popcount8 "$x")))
    for ((bit=7; bit>=0; bit--)); do
      row+="$(((x >> bit) & 1))"
    done
  done
  ROW_BITS="$row"
  ROW_USED="$row_used"
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

seed="$(tr -d '\r\n' < "$input")"
declare -A USED
used_total=0
for ((r=0; r<128; r++)); do
  knot_row "${seed}-${r}"
  used_total=$((used_total + ROW_USED))
  row="$ROW_BITS"
  for ((c=0; c<128; c++)); do
    if [[ "${row:c:1}" == "1" ]]; then
      USED["$r,$c"]=1
    fi
  done
done

if [[ "$part" == "1" ]]; then
  ans="$used_total"
else
  declare -A SEEN
  regions=0
  for ((r=0; r<128; r++)); do
    for ((c=0; c<128; c++)); do
      key="$r,$c"
      [[ -n "${USED[$key]:-}" ]] || continue
      [[ -z "${SEEN[$key]:-}" ]] || continue
      regions=$((regions + 1))
      declare -a QR QC
      head=0
      tail=0
      QR[tail]="$r"; QC[tail]="$c"; tail=$((tail + 1))
      SEEN["$key"]=1
      while (( head < tail )); do
        x="${QR[$head]}"
        y="${QC[$head]}"
        head=$((head + 1))
        for d in "1 0" "-1 0" "0 1" "0 -1"; do
          read -r dx dy <<<"$d"
          nx=$((x + dx))
          ny=$((y + dy))
          if (( nx < 0 || nx >= 128 || ny < 0 || ny >= 128 )); then
            continue
          fi
          nk="$nx,$ny"
          [[ -n "${USED[$nk]:-}" ]] || continue
          [[ -z "${SEEN[$nk]:-}" ]] || continue
          SEEN["$nk"]=1
          QR[tail]="$nx"
          QC[tail]="$ny"
          tail=$((tail + 1))
        done
      done
    done
  done
  ans="$regions"
fi

if [[ "$part" == "1" ]]; then expected="$EXPECTED_PART1"; else expected="$EXPECTED_PART2"; fi
[[ "$ans" == "$expected" ]] || { echo "answer mismatch: got $ans expected $expected" >&2; exit 3; }

echo "$ans"
end_ns=$(date +%s%N)
elapsed_ns=$((end_ns - start_ns))
ms_int=$((elapsed_ns / 1000000))
ms_frac=$(((elapsed_ns / 1000) % 1000))
printf "[bash-fancy] day=%d part=%d runtime_ms=%d.%03d\n" 14 "$part" "$ms_int" "$ms_frac" >&2
