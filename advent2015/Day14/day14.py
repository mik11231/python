#!/usr/bin/env python3
"""Advent of Code 2015 Day 14 - Reindeer Olympics."""

import re
from pathlib import Path

RACE_SECONDS = 2503


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


def distance_after(seconds: int, speed: int, fly_t: int, rest_t: int) -> int:
    """Total distance after `seconds` for one reindeer."""
    cycle = fly_t + rest_t
    full_cycles = seconds // cycle
    remainder = seconds % cycle
    flying_in_remainder = min(remainder, fly_t)
    total_fly = full_cycles * fly_t + flying_in_remainder
    return total_fly * speed


def solve(s: str) -> int:
    """Max distance any reindeer travels in RACE_SECONDS."""
    reindeer = parse(s)
    best = 0
    for name, speed, fly_t, rest_t in reindeer:
        d = distance_after(RACE_SECONDS, speed, fly_t, rest_t)
        best = max(best, d)
    return best


if __name__ == "__main__":
    text = Path(__file__).with_name("d14_input.txt").read_text(encoding="utf-8")
    print(solve(text))
