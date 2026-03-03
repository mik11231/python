"""Advent of Code 2018 solution module."""

import re
from collections import defaultdict
from pathlib import Path

LOG_RE = re.compile(r"\[(.+)] (.+)")
GUARD_RE = re.compile(r"Guard #(\d+) begins shift")


def load_lines(path: Path) -> list[str]:
    return sorted(line.strip() for line in path.read_text().splitlines() if line.strip())


def build_sleep_table(lines: list[str]) -> dict[int, list[int]]:
    minutes_by_guard: dict[int, list[int]] = defaultdict(lambda: [0] * 60)
    guard = None
    sleep_start = None

    for line in lines:
        _, action = LOG_RE.fullmatch(line).groups()
        minute = int(line[15:17])

        guard_match = GUARD_RE.fullmatch(action)
        if guard_match:
            guard = int(guard_match.group(1))
            continue
        if action == "falls asleep":
            sleep_start = minute
            continue
        if action == "wakes up":
            for m in range(sleep_start, minute):
                minutes_by_guard[guard][m] += 1

    return minutes_by_guard


def solve(lines: list[str]) -> int:
    minutes_by_guard = build_sleep_table(lines)
    best_guard = -1
    best_minute = -1
    best_count = -1

    for guard, minute_counts in minutes_by_guard.items():
        for minute, count in enumerate(minute_counts):
            if count > best_count:
                best_guard = guard
                best_minute = minute
                best_count = count

    return best_guard * best_minute


if __name__ == "__main__":
    input_path = Path(__file__).with_name("d4_input.txt")
    print(solve(load_lines(input_path)))
