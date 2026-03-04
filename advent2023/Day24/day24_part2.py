#!/usr/bin/env python3
"""Advent of Code 2023 Day 24 Part 2 - Never Tell Me The Odds.

Find a rock position (rx, ry, rz) and velocity (rvx, rvy, rvz) such that
the rock hits every hailstone.

This implementation avoids external dependencies by solving a 6x6 linear
system (with exact Fractions) derived from pairwise cross-product equations.
"""
from pathlib import Path
from fractions import Fraction
from itertools import combinations


def _cross(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    """
    Run `_cross` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: a, b.
    - Returns the computed result for this stage of the pipeline.
    """
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _pair_equations(
    p1: tuple[int, int, int],
    v1: tuple[int, int, int],
    p2: tuple[int, int, int],
    v2: tuple[int, int, int],
) -> tuple[list[list[int]], list[int]]:
    """
    Run `_pair_equations` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: p1, v1, p2, v2.
    - Returns the computed result for this stage of the pipeline.
    """
    dv = (v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])
    dp = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
    rhs = tuple(a - b for a, b in zip(_cross(p2, v2), _cross(p1, v1)))
    a, b, c = dv
    d, e, f = dp

    # Unknown vector is [rx, ry, rz, rvx, rvy, rvz]
    mat = [
        [0, c, -b, 0, -f, e],
        [-c, 0, a, f, 0, -d],
        [b, -a, 0, -e, d, 0],
    ]
    return mat, [rhs[0], rhs[1], rhs[2]]


def _solve_linear_6x6(mat: list[list[int]], rhs: list[int]) -> list[Fraction]:
    """
    Run `_solve_linear_6x6` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: mat, rhs.
    - Returns the computed result for this stage of the pipeline.
    """
    aug: list[list[Fraction]] = [
        [Fraction(v) for v in row] + [Fraction(rhs[i])] for i, row in enumerate(mat)
    ]
    n = 6
    row = 0
    for col in range(n):
        pivot = None
        for r in range(row, n):
            if aug[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            continue
        aug[row], aug[pivot] = aug[pivot], aug[row]
        pv = aug[row][col]
        aug[row] = [x / pv for x in aug[row]]
        for r in range(n):
            if r == row or aug[r][col] == 0:
                continue
            factor = aug[r][col]
            aug[r] = [aug[r][c] - factor * aug[row][c] for c in range(n + 1)]
        row += 1
        if row == n:
            break
    if row < n:
        raise ValueError("Singular system")
    return [aug[i][n] for i in range(n)]


def solve(s: str) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s.
    - Returns the computed result for this stage of the pipeline.
    """
    stones = []
    for line in s.strip().splitlines():
        pos, vel = line.split("@")
        px, py, pz = map(int, pos.split(","))
        vx, vy, vz = map(int, vel.split(","))
        stones.append((px, py, pz, vx, vy, vz))
    for ia, ib, ic in combinations(range(len(stones)), 3):
        p1 = stones[ia][:3]
        v1 = stones[ia][3:]
        p2 = stones[ib][:3]
        v2 = stones[ib][3:]
        p3 = stones[ic][:3]
        v3 = stones[ic][3:]
        m1, b1 = _pair_equations(p1, v1, p2, v2)
        m2, b2 = _pair_equations(p1, v1, p3, v3)
        mat = m1 + m2
        rhs = b1 + b2
        try:
            sol = _solve_linear_6x6(mat, rhs)
        except ValueError:
            continue
        rx, ry, rz, *_ = sol
        if rx.denominator == 1 and ry.denominator == 1 and rz.denominator == 1:
            return int(rx + ry + rz)
    raise RuntimeError("Could not solve rock trajectory")


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d24_input.txt").read_text()))
