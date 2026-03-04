#!/usr/bin/env bash
set -euo pipefail
EXPECTED_SHA='09a2c42b5b2f5e7e0c325a89194f42c2a9f88efb35cd6dcf61a69005545cc3d1'
EXPECTED_PART1='685'
EXPECTED_PART2='1457'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day11/d11_input.txt" "Day11/d11_input.txt" "../Day11/d11_input.txt" "../../Day11/d11_input.txt"; do
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

raw="$(tr -d '\r\n' < "$input")"

ans="$({
  awk -v part="$part" -v s="$raw" '
    function abs(v) { return v < 0 ? -v : v }
    function dist(x,y,z,    a,b,c,m) {
      a = abs(x); b = abs(y); c = abs(z)
      m = a; if (b > m) m = b; if (c > m) m = c
      return m
    }
    BEGIN {
      x = y = z = 0
      best = 0
      n = split(s, step, ",")
      for (i = 1; i <= n; i++) {
        d = step[i]
        if (d == "n") { y++; z-- }
        else if (d == "ne") { x++; z-- }
        else if (d == "se") { x++; y-- }
        else if (d == "s") { y--; z++ }
        else if (d == "sw") { x--; z++ }
        else if (d == "nw") { x--; y++ }
        cur = dist(x,y,z)
        if (cur > best) best = cur
      }
      if (part == 1) print dist(x,y,z)
      else print best
    }
  '
})"

if [[ "$part" == "1" ]]; then expected="$EXPECTED_PART1"; else expected="$EXPECTED_PART2"; fi
[[ "$ans" == "$expected" ]] || { echo "answer mismatch: got $ans expected $expected" >&2; exit 3; }

echo "$ans"
end_ns=$(date +%s%N)
elapsed_ns=$((end_ns - start_ns))
ms_int=$((elapsed_ns / 1000000))
ms_frac=$(((elapsed_ns / 1000) % 1000))
ms="$(printf "%d.%03d" "$ms_int" "$ms_frac")"
printf "[bash-fancy] day=%d part=%d runtime_ms=%.3f\n" 11 "$part" "$ms" >&2
