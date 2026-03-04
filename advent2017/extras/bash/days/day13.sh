#!/usr/bin/env bash
set -euo pipefail
EXPECTED_SHA='b59ed1486b6ec731cb7c2f55fdfec971d1157b9411fb823f9ddf0a3839d12cc8'
EXPECTED_PART1='2604'
EXPECTED_PART2='3941460'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day13/d13_input.txt" "Day13/d13_input.txt" "../Day13/d13_input.txt" "../../Day13/d13_input.txt"; do
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
    BEGIN { n = 0 }
    {
      gsub(/ /, "")
      split($0, p, ":")
      d[n] = p[1] + 0
      r[n] = p[2] + 0
      per[n] = 2 * (r[n] - 1)
      n++
    }
    END {
      if (part == 1) {
        sev = 0
        for (i = 0; i < n; i++) if (d[i] % per[i] == 0) sev += d[i] * r[i]
        print sev
        exit
      }

      delay = 0
      while (1) {
        ok = 1
        for (i = 0; i < n; i++) {
          if ((delay + d[i]) % per[i] == 0) {
            ok = 0
            break
          }
        }
        if (ok) {
          print delay
          exit
        }
        delay++
      }
    }
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
printf "[bash-fancy] day=%d part=%d runtime_ms=%.3f\n" 13 "$part" "$ms" >&2
