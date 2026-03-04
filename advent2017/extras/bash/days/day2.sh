#!/usr/bin/env bash
set -euo pipefail
EXPECTED_SHA='c64165a1af8ab4877e736a095bde2b22d523468077099fab5a338f53b0059681'
EXPECTED_PART1='36174'
EXPECTED_PART2='244'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day2/d2_input.txt" "Day2/d2_input.txt" "../Day2/d2_input.txt" "../../Day2/d2_input.txt"; do
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

ans="$({
  awk -v part="$part" '
    function part1(line,    i, n, minv, maxv, v) {
      n = split(line, a, /[[:space:]]+/)
      minv = a[1] + 0
      maxv = a[1] + 0
      for (i = 2; i <= n; i++) {
        v = a[i] + 0
        if (v < minv) minv = v
        if (v > maxv) maxv = v
      }
      return maxv - minv
    }
    function part2(line,    i, j, n, x, y) {
      n = split(line, a, /[[:space:]]+/)
      for (i = 1; i <= n; i++) {
        x = a[i] + 0
        for (j = 1; j <= n; j++) {
          if (i == j) continue
          y = a[j] + 0
          if (y != 0 && x % y == 0) return int(x / y)
        }
      }
      return 0
    }
    {
      gsub(/^ +| +$/, "", $0)
      if ($0 == "") next
      if (part == 1) sum += part1($0)
      else sum += part2($0)
    }
    END { print sum }
  ' "$input"
})"

if [[ "$part" == "1" ]]; then expected="$EXPECTED_PART1"; else expected="$EXPECTED_PART2"; fi
[[ "$ans" == "$expected" ]] || { echo "answer mismatch: got $ans expected $expected" >&2; exit 3; }

echo "$ans"
end_ns=$(date +%s%N)
elapsed_ns=$((end_ns - start_ns))
ms_int=$((elapsed_ns / 1000000))
ms_frac=$(((elapsed_ns / 1000) % 1000))
ms="$(printf "%d.%03d" "$ms_int" "$ms_frac")"
printf "[bash-fancy] day=%d part=%d runtime_ms=%.3f\n" 2 "$part" "$ms" >&2
