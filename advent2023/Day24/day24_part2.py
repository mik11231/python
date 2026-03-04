#!/usr/bin/env python3
"""Advent of Code 2023 Day 24 Part 2 - Never Tell Me The Odds.

Find a rock position (rx, ry, rz) and velocity (rvx, rvy, rvz) such that
the rock hits every hailstone. Use sympy to solve the system of equations
derived from the first 3 hailstones (9 equations, 9 unknowns).
"""
from pathlib import Path
import sympy


def solve(s: str) -> int:
    stones = []
    for line in s.strip().splitlines():
        pos, vel = line.split("@")
        px, py, pz = map(int, pos.split(","))
        vx, vy, vz = map(int, vel.split(","))
        stones.append((px, py, pz, vx, vy, vz))

    rx, ry, rz, rvx, rvy, rvz = sympy.symbols("rx ry rz rvx rvy rvz")
    equations = []
    time_vars = []

    for i in range(3):
        px, py, pz, vx, vy, vz = stones[i]
        t = sympy.Symbol(f"t{i}")
        time_vars.append(t)
        equations.append(rx + rvx * t - px - vx * t)
        equations.append(ry + rvy * t - py - vy * t)
        equations.append(rz + rvz * t - pz - vz * t)

    sol = sympy.solve(equations, [rx, ry, rz, rvx, rvy, rvz] + time_vars)

    if isinstance(sol, list):
        sol = sol[0]
        return int(sol[0] + sol[1] + sol[2])
    return int(sol[rx] + sol[ry] + sol[rz])


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d24_input.txt").read_text()))
