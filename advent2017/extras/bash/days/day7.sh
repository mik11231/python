#!/usr/bin/env bash
# Architecture Notes:
# - This script is documented so operators can rebuild behavior from comments alone.
# - Structure follows: input acquisition -> normalization -> solving -> reporting.
# - Keep side effects explicit and measured in runtime/benchmark workflows.

set -euo pipefail
EXPECTED_SHA='3fd999ac97824b5f8cd2bcbf5c69704a352a0a4bbf9735b0fcc289932fcaeac6'
EXPECTED_PART1='mwzaxaj'
EXPECTED_PART2='1219'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day7/d7_input.txt" "Day7/d7_input.txt" "../Day7/d7_input.txt" "../../Day7/d7_input.txt"; do
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
    function parse_line(line,    pos,left,right,m,n,i,c) {
      pos = index(line, "->")
      if (pos > 0) {
        left = substr(line, 1, pos - 1)
        right = substr(line, pos + 2)
      } else {
        left = line
        right = ""
      }

      if (match(left, /^([a-z]+) \(([0-9]+)\)/, m)) {
        name = m[1]
        weight[name] = m[2] + 0
        nodes[name] = 1
      }

      gsub(/^ +| +$/, "", right)
      gsub(/, +/, " ", right)
      kids[name] = right

      if (right != "") {
        n = split(right, arr, / +/)
        for (i = 1; i <= n; i++) {
          c = arr[i]
          if (c != "") parent[c] = name
        }
      }
    }

    function root_name(    n) {
      for (n in nodes) if (!(n in parent)) return n
      return ""
    }

    function map_count(m,    k,c) { c=0; for (k in m) c++; return c }

    function total(n,    arr,m,i,c,sum) {
      if (n in memo) return memo[n]
      sum = weight[n]
      if (kids[n] != "") {
        m = split(kids[n], arr, / +/)
        for (i = 1; i <= m; i++) {
          c = arr[i]
          if (c != "") sum += total(c)
        }
      }
      memo[n] = sum
      return sum
    }

    function find_fix(n,    arr,m,i,c,t,unique_t,common_t,unique_c,deeper,delta) {
      if (kids[n] == "") return ""

      delete cnt
      delete child_by_t
      m = split(kids[n], arr, / +/)
      for (i = 1; i <= m; i++) {
        c = arr[i]
        if (c == "") continue
        t = total(c)
        cnt[t]++
        child_by_t[t] = c
      }

      if (map_count(cnt) <= 1) return ""

      for (t in cnt) {
        if (cnt[t] == 1) {
          unique_t = t
          unique_c = child_by_t[t]
        } else {
          common_t = t
        }
      }

      deeper = find_fix(unique_c)
      if (deeper != "") return deeper

      delta = common_t - unique_t
      return weight[unique_c] + delta
    }

    {
      if ($0 !~ /^[[:space:]]*$/) parse_line($0)
    }
    END {
      root = root_name()
      if (part == 1) {
        print root
        exit
      }
      fix = find_fix(root)
      print fix
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
printf "[bash-fancy] day=%d part=%d runtime_ms=%.3f\n" 7 "$part" "$ms" >&2
