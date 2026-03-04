#!/usr/bin/env bash
set -euo pipefail
EXPECTED_SHA='36d753e40c996a2ec1083c34b8cda3ffa986bc63a44d73be5ee1ed81084c6401'
EXPECTED_PART1='451'
EXPECTED_PART2='223'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day4/d4_input.txt" "Day4/d4_input.txt" "../Day4/d4_input.txt" "../../Day4/d4_input.txt"; do
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
    function clear_seen(    k) { for (k in seen) delete seen[k] }
    {
      gsub(/^ +| +$/, "", $0)
      if ($0 == "") next
      clear_seen()
      n = split($0, w, /[[:space:]]+/)
      ok = 1
      for (i = 1; i <= n; i++) {
        key = w[i]
        if (part == 2) {
          split("", cnt)
          for (j = 1; j <= length(key); j++) {
            ch = substr(key, j, 1)
            cnt[ch]++
          }
          key = ""
          for (c = 97; c <= 122; c++) {
            ch = sprintf("%c", c)
            if (cnt[ch] > 0) key = key ch cnt[ch] "#"
          }
        }
        if (key in seen) { ok = 0; break }
        seen[key] = 1
      }
      total += ok
    }
    END { print total }
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
printf "[bash-fancy] day=%d part=%d runtime_ms=%.3f\n" 4 "$part" "$ms" >&2
