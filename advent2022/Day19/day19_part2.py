#!/usr/bin/env python3
"""Advent of Code 2022 Day 19 Part 2.

Same blueprint optimization as Part 1 but with 32 minutes and only the first
3 blueprints. Returns the product of max geodes for those three.

This version uses a "jump" DFS: instead of simulating each minute with a wait
action branch, it jumps directly to the next minute where a selected robot can
be built. Combined with memoization and resource/robot caps, this is fast
enough for full-repo verification under normal timeouts.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import re


def ceil_div(a: int, b: int) -> int:
    """Return ceil(a / b) for non-negative integers and b > 0."""
    return (a + b - 1) // b


def best(bp: tuple[int, int, int, int, int, int], minutes: int) -> int:
    """Return max geodes for one blueprint within the given minutes."""
    ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs = bp
    max_ore = max(ore_ore, clay_ore, obs_ore, geo_ore)
    max_clay = obs_clay
    max_obs = geo_obs

    @lru_cache(maxsize=None)
    def dfs(
        t: int,
        ore: int,
        clay: int,
        obs: int,
        ro: int,
        rc: int,
        rb: int,
        rg: int,
    ) -> int:
        """
        Run `dfs` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: t, ore, clay, obs, ro, rc, rb, rg.
        - Returns the computed result for this stage of the pipeline.
        """
        if t <= 0:
            return 0

        # Cap carry-over resources to the maximum spendable amount.
        ore = min(ore, max_ore * t)
        clay = min(clay, max_clay * t)
        obs = min(obs, max_obs * t)

        # Option: build nothing else.
        best_geodes = rg * t

        # Try building a geode robot.
        if rb > 0:
            wait = max(
                0 if ore >= geo_ore else ceil_div(geo_ore - ore, ro),
                0 if obs >= geo_obs else ceil_div(geo_obs - obs, rb),
            )
            nt = t - wait - 1
            if nt >= 0:
                nore = ore + ro * (wait + 1) - geo_ore
                nclay = clay + rc * (wait + 1)
                nobs = obs + rb * (wait + 1) - geo_obs
                best_geodes = max(
                    best_geodes,
                    rg * (wait + 1) + dfs(nt, nore, nclay, nobs, ro, rc, rb, rg + 1),
                )

        # Try building an obsidian robot.
        if rc > 0 and rb < max_obs:
            wait = max(
                0 if ore >= obs_ore else ceil_div(obs_ore - ore, ro),
                0 if clay >= obs_clay else ceil_div(obs_clay - clay, rc),
            )
            nt = t - wait - 1
            if nt >= 0:
                nore = ore + ro * (wait + 1) - obs_ore
                nclay = clay + rc * (wait + 1) - obs_clay
                nobs = obs + rb * (wait + 1)
                best_geodes = max(
                    best_geodes,
                    rg * (wait + 1) + dfs(nt, nore, nclay, nobs, ro, rc, rb + 1, rg),
                )

        # Try building a clay robot.
        if rc < max_clay:
            wait = 0 if ore >= clay_ore else ceil_div(clay_ore - ore, ro)
            nt = t - wait - 1
            if nt >= 0:
                nore = ore + ro * (wait + 1) - clay_ore
                nclay = clay + rc * (wait + 1)
                nobs = obs + rb * (wait + 1)
                best_geodes = max(
                    best_geodes,
                    rg * (wait + 1) + dfs(nt, nore, nclay, nobs, ro, rc + 1, rb, rg),
                )

        # Try building an ore robot.
        if ro < max_ore:
            wait = 0 if ore >= ore_ore else ceil_div(ore_ore - ore, ro)
            nt = t - wait - 1
            if nt >= 0:
                nore = ore + ro * (wait + 1) - ore_ore
                nclay = clay + rc * (wait + 1)
                nobs = obs + rb * (wait + 1)
                best_geodes = max(
                    best_geodes,
                    rg * (wait + 1) + dfs(nt, nore, nclay, nobs, ro + 1, rc, rb, rg),
                )

        return best_geodes

    return dfs(minutes, 0, 0, 0, 1, 0, 0, 0)


def solve(s: str) -> int:
    """Parse first 3 blueprints and return product of their max geodes at 32 min."""
    bps: list[tuple[int, int, int, int, int, int]] = []
    for ln in s.splitlines()[:3]:
        if not ln:
            continue
        _, oo, co, bo, bc, go, gob = map(int, re.findall(r"\d+", ln))
        bps.append((oo, co, bo, bc, go, gob))
    ans = 1
    for bp in bps:
        ans *= best(bp, 32)
    return ans


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d19_input.txt").read_text()))
