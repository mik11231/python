#!/usr/bin/env python3
"""Advent of Code 2025 - Day 10: Factory (Part 2)

Joltage mode: each button press adds +1 to a subset of counters.
For each machine, we find the minimum total presses to reach its target counters.

This implementation treats each machine as a small integer linear program and
solves it with PuLP (CBC), which is fast and exact for these sizes.
"""

from __future__ import annotations
from pathlib import Path

import re
from fractions import Fraction
from typing import Sequence

try:
    import pulp  # type: ignore
except Exception:
    pulp = None

LINE_RE = re.compile(r"\[([.#]+)\](.*)")


def parse_machine_line_joltage(line: str) -> tuple[list[int], list[list[int]]]:
    """Parse one line into (targets, buttons-as-index-lists)."""
    line = line.strip()
    if not line:
        raise ValueError("Empty line")

    m = LINE_RE.search(line)
    if not m:
        raise ValueError(f"Cannot parse: {line}")

    # Buttons: indices in parentheses.
    button_indices: list[list[int]] = []
    for group in re.findall(r"\(([^)]*)\)", m.group(2)):
        group = group.strip()
        if not group:
            continue
        inds = [int(part.strip()) for part in group.split(",") if part.strip()]
        if inds:
            button_indices.append(inds)

    # Joltage targets: numbers in curly braces.
    brace = re.search(r"\{([^}]*)\}", line)
    if not brace:
        raise ValueError("No joltage block")
    targets = [int(p.strip()) for p in brace.group(1).split(",") if p.strip()]
    return targets, button_indices


def min_presses_joltage(targets: Sequence[int], buttons: Sequence[Sequence[int]]) -> int:
    """Solve one machine's joltage problem exactly.

    Uses PuLP when available, otherwise falls back to an exact DFS+memo search.
    """
    t = list(targets)
    m = len(t)
    if m == 0 or all(v == 0 for v in t):
        return 0

    # Normalize buttons: clamp indices and drop empties
    norm_buttons: list[list[int]] = []
    for b in buttons:
        inds = sorted({i for i in b if 0 <= i < m})
        if inds:
            norm_buttons.append(inds)
    if not norm_buttons:
        raise RuntimeError("Machine has positive targets but no usable buttons")

    if pulp is None:
        # Solve A x = t, x >= 0 integer, minimizing sum(x).
        # For this puzzle input, nullity is small (<=3), so we can enumerate free vars exactly.
        k = len(norm_buttons)
        A = [[1 if i in norm_buttons[j] else 0 for j in range(k)] for i in range(m)]
        aug = [[Fraction(v) for v in row] + [Fraction(t[i])] for i, row in enumerate(A)]

        pivot_cols: list[int] = []
        row = 0
        for col in range(k):
            pivot = None
            for r in range(row, m):
                if aug[r][col] != 0:
                    pivot = r
                    break
            if pivot is None:
                continue
            aug[row], aug[pivot] = aug[pivot], aug[row]
            pv = aug[row][col]
            aug[row] = [x / pv for x in aug[row]]
            for r in range(m):
                if r == row or aug[r][col] == 0:
                    continue
                f = aug[r][col]
                aug[r] = [aug[r][c] - f * aug[row][c] for c in range(k + 1)]
            pivot_cols.append(col)
            row += 1
            if row == m:
                break

        for r in range(row, m):
            if aug[r][k] != 0:
                raise RuntimeError("Inconsistent joltage system")

        free_cols = [c for c in range(k) if c not in set(pivot_cols)]
        # Bound free vars by target rows they touch.
        upper: dict[int, int] = {}
        for f in free_cols:
            touched = [t[i] for i in range(m) if A[i][f] == 1]
            upper[f] = min(touched) if touched else 0

        pivot_row = {pc: r for r, pc in enumerate(pivot_cols)}
        best = 10**18
        free_vals: dict[int, int] = {}

        def search(idx: int) -> None:
            nonlocal best
            if idx == len(free_cols):
                x: list[Fraction] = [Fraction(0) for _ in range(k)]
                for f in free_cols:
                    x[f] = Fraction(free_vals[f])
                for p in pivot_cols:
                    r = pivot_row[p]
                    val = aug[r][k]
                    for f in free_cols:
                        val -= aug[r][f] * x[f]
                    if val < 0 or val.denominator != 1:
                        return
                    x[p] = val
                total = sum(int(v) for v in x)
                if total < best:
                    best = total
                return

            f = free_cols[idx]
            ub = upper[f]
            for v in range(ub + 1):
                free_vals[f] = v
                search(idx + 1)

        search(0)
        if best >= 10**18:
            raise RuntimeError("No exact non-negative integer solution")
        return best

    k = len(norm_buttons)

    prob = pulp.LpProblem("aoc2025_day10_part2_machine", pulp.LpMinimize)
    x = [pulp.LpVariable(f"x_{j}", lowBound=0, cat="Integer") for j in range(k)]

    # Constraints: for each counter i, sum of presses affecting it equals target
    for i in range(m):
        prob += (
            pulp.lpSum(x[j] for j, inds in enumerate(norm_buttons) if i in inds) == t[i]
        ), f"counter_{i}"

    # Objective: minimize total presses
    prob += pulp.lpSum(x), "total_presses"

    # Solve with CBC (default PuLP solver)
    status = prob.solve(pulp.PULP_CBC_CMD(msg=False))
    if pulp.LpStatus[status] != "Optimal":
        raise RuntimeError(f"ILP solver failed with status {pulp.LpStatus[status]}")

    total_presses = int(round(pulp.value(pulp.lpSum(x))))
    return total_presses


def _solve_one_line(line: str) -> int:
    """Parse one line and return min presses."""
    line = line.strip()
    if not line:
        return 0
    targets, buttons = parse_machine_line_joltage(line)
    return min_presses_joltage(targets, buttons)


def solve() -> int:
    """Solve Part 2: sum of min presses over all machines (sequential ILP per machine)."""
    input_path = Path(__file__).resolve().parent / "d10_input.txt"
    lines = [ln.strip() for ln in input_path.read_text(encoding="utf-8").splitlines() if ln.strip()]

    total = 0
    for ln in lines:
        total += _solve_one_line(ln)
    return total


if __name__ == "__main__":
    result = solve()
    print(f"Total fewest button presses (Part 2): {result}")
