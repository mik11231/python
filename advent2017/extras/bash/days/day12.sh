#!/usr/bin/env bash
# Architecture Notes:
# - This script is documented so operators can rebuild behavior from comments alone.
# - Structure follows: input acquisition -> normalization -> solving -> reporting.
# - Keep side effects explicit and measured in runtime/benchmark workflows.

set -euo pipefail
EXPECTED_SHA='5a807a689f833a1add89ef7c1215b693721849db8347b273bca570346357377c'
EXPECTED_PART1='239'
EXPECTED_PART2='215'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day12/d12_input.txt" "Day12/d12_input.txt" "../Day12/d12_input.txt" "../../Day12/d12_input.txt"; do
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
    function push(qname, v) { q[qtail++] = v }
    function pop() { return q[qhead++] }
    function bfs(start,    u,m,i,v,nbrs,cnt) {
      if (seen[start]) return 0
      qhead = qtail = 0
      push("q", start)
      seen[start] = 1
      cnt = 0
      while (qhead < qtail) {
        u = pop()
        cnt++
        m = split(adj[u], nbrs, /,/) 
        for (i = 1; i <= m; i++) {
          v = nbrs[i] + 0
          if (!seen[v]) {
            seen[v] = 1
            push("q", v)
          }
        }
      }
      return cnt
    }
    {
      gsub(/ /, "")
      split($0, p, "<->")
      u = p[1] + 0
      adj[u] = p[2]
      nodes[u] = 1
    }
    END {
      c0 = bfs(0)
      groups = 1
      for (u in nodes) {
        if (!seen[u]) {
          bfs(u)
          groups++
        }
      }
      if (part == 1) print c0
      else print groups
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
printf "[bash-fancy] day=%d part=%d runtime_ms=%.3f\n" 12 "$part" "$ms" >&2
