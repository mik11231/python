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
    sleepiest_guard = max(minutes_by_guard, key=lambda gid: sum(minutes_by_guard[gid]))
    best_minute = max(range(60), key=lambda m: minutes_by_guard[sleepiest_guard][m])
    return sleepiest_guard * best_minute


if __name__ == "__main__":
    input_path = Path(__file__).with_name("d4_input.txt")
    print(solve(load_lines(input_path)))
