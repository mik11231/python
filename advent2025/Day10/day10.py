#!/usr/bin/env python3
"""Advent of Code 2025 - Day 10: Factory (Part 1)"""

from pathlib import Path
import re
from collections import deque


LINE_RE = re.compile(r"\[([.#]+)\](.*)\{")


def parse_machine_line(line: str):
    """Parse one machine description line into (num_lights, target_mask, button_masks)."""
    line = line.strip()
    if not line:
        return None

    m = LINE_RE.search(line)
    if not m:
        raise ValueError(f"Cannot parse line: {line}")

    pattern = m.group(1)
    rest = m.group(2)

    num_lights = len(pattern)
    target_mask = 0
    for i, ch in enumerate(pattern):
        if ch == "#":
            target_mask |= 1 << i

    button_masks = []
    for group in re.findall(r"\(([^)]*)\)", rest):
        group = group.strip()
        if not group:
            continue
        mask = 0
        for part in group.split(","):
            part = part.strip()
            if not part:
                continue
            idx = int(part)
            mask |= 1 << idx
        button_masks.append(mask)

    return num_lights, target_mask, button_masks


def min_presses(num_lights: int, target_mask: int, button_masks: list[int]) -> int:
    """Fewest button presses to reach target_mask starting from all-off."""
    if target_mask == 0:
        return 0

    max_state = 1 << num_lights
    dist = [-1] * max_state
    start = 0
    dist[start] = 0
    q: deque[int] = deque([start])

    while q:
        state = q.popleft()
        d = dist[state]
        for mask in button_masks:
            next_state = state ^ mask
            if dist[next_state] != -1:
                continue
            nd = d + 1
            if next_state == target_mask:
                return nd
            dist[next_state] = nd
            q.append(next_state)

    raise RuntimeError(f"Target state {target_mask} unreachable for {num_lights} lights")


def solve() -> int:
    """Solve Day 10 Part 1 for the real input."""
    input_path = Path(__file__).with_name('d10_input.txt')
    total = 0

    with input_path.open("r", encoding="utf-8") as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            parsed = parse_machine_line(raw)
            if parsed is None:
                continue
            num_lights, target_mask, button_masks = parsed
            presses = min_presses(num_lights, target_mask, button_masks)
            total += presses

    return total


if __name__ == "__main__":
    result = solve()
    print(f"Total fewest button presses (Part 1): {result}")

