#!/usr/bin/env python3
"""Advent of Code 2015 Day 14 Part 2 - Points to reindeer in the lead each second."""

import re
from pathlib import Path

RACE_SECONDS = 2503


def distance_after(seconds: int, speed: int, fly_t: int, rest_t: int) -> int:
    """Total distance after `seconds` for one reindeer."""
    cycle = fly_t + rest_t
    full_cycles = seconds // cycle
    remainder = seconds % cycle
    flying_in_remainder = min(remainder, fly_t)
    total_fly = full_cycles * fly_t + flying_in_remainder
    return total_fly * speed


def parse(s: str) -> list[tuple[str, int, int, int]]:
    """Parse input. Returns list of (name, speed_km_s, fly_seconds, rest_seconds)."""
    pattern = re.compile(
        r"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds\."
    )
    reindeer = []
    for line in s.strip().splitlines():
        m = pattern.match(line.strip())
        if not m:
            continue
        name, speed, fly_t, rest_t = m.groups()
        reindeer.append((name, int(speed), int(fly_t), int(rest_t)))
    return reindeer


def solve(s: str) -> int:
    """After each second, award 1 point to reindeer(s) in the lead. Return max points."""
    reindeer = parse(s)
    n = len(reindeer)
    points = [0] * n
    for sec in range(1, RACE_SECONDS + 1):
        dists = [
            distance_after(sec, speed, fly_t, rest_t)
            for _, speed, fly_t, rest_t in reindeer
        ]
        best = max(dists)
        for i in range(n):
            if dists[i] == best:
                points[i] += 1
    return max(points)


if __name__ == "__main__":
    text = Path(__file__).with_name("d14_input.txt").read_text(encoding="utf-8")
    print(solve(text))
