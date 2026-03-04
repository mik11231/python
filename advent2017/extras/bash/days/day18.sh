#!/usr/bin/env bash
set -euo pipefail
EXPECTED_SHA='4052bdd33baaf7be897365aa3ad1cff5fae76ade4c474c9e5ebcdf5058ad368e'
EXPECTED_PART1='7071'
EXPECTED_PART2='8001'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
default_input() {
  for c in "advent2017/Day18/d18_input.txt" "Day18/d18_input.txt" "../Day18/d18_input.txt" "../../Day18/d18_input.txt"; do
    [[ -f "$c" ]] && echo "$c" && return 0
  done
  echo "input not found" >&2; exit 1
}

is_int() { [[ "$1" =~ ^-?[0-9]+$ ]]; }
val1() {
  local t="$1"
  if is_int "$t"; then
    echo "$t"
  else
    echo "${R[$t]:-0}"
  fi
}

valn() {
  local map_name="$1"
  local t="$2"
  declare -n M="$map_name"
  if is_int "$t"; then
    echo "$t"
  else
    echo "${M[$t]:-0}"
  fi
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

declare -a OP X Y
while IFS= read -r line || [[ -n "$line" ]]; do
  [[ -n "${line// }" ]] || continue
  read -r op a b <<<"$line"
  OP+=("$op")
  X+=("$a")
  Y+=("${b:-0}")
done < "$input"
n="${#OP[@]}"

if [[ "$part" == "1" ]]; then
  declare -A R
  ip=0
  snd=0
  while (( ip >= 0 && ip < n )); do
    op="${OP[$ip]}"
    x="${X[$ip]}"
    y="${Y[$ip]}"
    case "$op" in
      snd)
        snd="$(val1 "$x")"
        ;;
      set)
        R["$x"]="$(val1 "$y")"
        ;;
      add)
        R["$x"]=$(( ${R[$x]:-0} + $(val1 "$y") ))
        ;;
      mul)
        R["$x"]=$(( ${R[$x]:-0} * $(val1 "$y") ))
        ;;
      mod)
        R["$x"]=$(( ${R[$x]:-0} % $(val1 "$y") ))
        ;;
      rcv)
        if (( $(val1 "$x") != 0 )); then
          ans="$snd"
          break
        fi
        ;;
      jgz)
        if (( $(val1 "$x") > 0 )); then
          ip=$((ip + $(val1 "$y")))
          continue
        fi
        ;;
    esac
    ip=$((ip + 1))
  done
else
  declare -A R0 R1
  R0[p]=0
  R1[p]=1
  ip0=0
  ip1=0
  done0=0
  done1=0
  wait0=0
  wait1=0
  sent1=0
  declare -a Q0 Q1
  h0=0
  h1=0
  t0=0
  t1=0

  PROGRESSED=0
  step_prog() {
    local pid="$1"
    local map_name ip_var done_var wait_var in_h_var
    if (( pid == 0 )); then
      map_name="R0"; ip_var="ip0"; done_var="done0"; wait_var="wait0"; in_h_var="h0"
    else
      map_name="R1"; ip_var="ip1"; done_var="done1"; wait_var="wait1"; in_h_var="h1"
    fi
    declare -n M="$map_name"
    declare -n IP="$ip_var"
    declare -n DONE="$done_var"
    declare -n WAIT="$wait_var"
    declare -n INH="$in_h_var"
    PROGRESSED=0

    if (( IP < 0 || IP >= n )); then
      DONE=1
      WAIT=1
      PROGRESSED=0
      return
    fi

    op="${OP[$IP]}"
    x="${X[$IP]}"
    y="${Y[$IP]}"
    case "$op" in
      snd)
        if (( pid == 0 )); then
          Q1[$t1]="$(valn "$map_name" "$x")"
          t1=$((t1 + 1))
        else
          Q0[$t0]="$(valn "$map_name" "$x")"
          t0=$((t0 + 1))
          sent1=$((sent1 + 1))
        fi
        IP=$((IP + 1))
        WAIT=0
        PROGRESSED=1
        ;;
      set)
        M["$x"]="$(valn "$map_name" "$y")"
        IP=$((IP + 1))
        WAIT=0
        PROGRESSED=1
        ;;
      add)
        M["$x"]=$(( ${M[$x]:-0} + $(valn "$map_name" "$y") ))
        IP=$((IP + 1))
        WAIT=0
        PROGRESSED=1
        ;;
      mul)
        M["$x"]=$(( ${M[$x]:-0} * $(valn "$map_name" "$y") ))
        IP=$((IP + 1))
        WAIT=0
        PROGRESSED=1
        ;;
      mod)
        M["$x"]=$(( ${M[$x]:-0} % $(valn "$map_name" "$y") ))
        IP=$((IP + 1))
        WAIT=0
        PROGRESSED=1
        ;;
      rcv)
        if (( pid == 0 )); then
          if (( h0 < t0 )); then
            M["$x"]="${Q0[$h0]}"
            h0=$((h0 + 1))
            IP=$((IP + 1))
            WAIT=0
            PROGRESSED=1
          else
            WAIT=1
          fi
        else
          if (( h1 < t1 )); then
            M["$x"]="${Q1[$h1]}"
            h1=$((h1 + 1))
            IP=$((IP + 1))
            WAIT=0
            PROGRESSED=1
          else
            WAIT=1
          fi
        fi
        ;;
      jgz)
        if (( $(valn "$map_name" "$x") > 0 )); then
          IP=$((IP + $(valn "$map_name" "$y")))
        else
          IP=$((IP + 1))
        fi
        WAIT=0
        PROGRESSED=1
        ;;
    esac
  }

  while :; do
    step_prog 0
    p0="$PROGRESSED"
    step_prog 1
    p1="$PROGRESSED"
    if (( p0 == 0 && p1 == 0 )) && (( (wait0 || done0) && (wait1 || done1) )); then
      ans="$sent1"
      break
    fi
  done
fi

if [[ "$part" == "1" ]]; then expected="$EXPECTED_PART1"; else expected="$EXPECTED_PART2"; fi
[[ "$ans" == "$expected" ]] || { echo "answer mismatch: got $ans expected $expected" >&2; exit 3; }

echo "$ans"
end_ns=$(date +%s%N)
elapsed_ns=$((end_ns - start_ns))
ms_int=$((elapsed_ns / 1000000))
ms_frac=$(((elapsed_ns / 1000) % 1000))
printf "[bash-fancy] day=%d part=%d runtime_ms=%d.%03d\n" 18 "$part" "$ms_int" "$ms_frac" >&2
