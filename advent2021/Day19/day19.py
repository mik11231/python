#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 19: Beacon Scanner (Part 1)

Multiple scanners each report beacon positions relative to themselves, and
each scanner may be in any of 24 orientations (the rotation group of a cube).
Two scanners overlap if they share at least 12 beacons.  Assemble all scanner
frames into a global frame (scanner 0's) and count total unique beacons.

Algorithm
---------
1. Pre-compute all 24 rotation functions for 3-D points.
2. BFS from scanner 0 (the reference frame).  For each newly resolved
   scanner, try to match every remaining unresolved scanner by:
   a. Rotating the unresolved scanner's beacons through all 24 orientations.
   b. For each orientation, computing the translation offset between every
      pair of beacons (one resolved, one candidate) and checking if any
      offset appears >= 12 times.
3. When a match is found, translate the candidate's beacons into the global
   frame and enqueue that scanner for further matching.
4. Repeat until all scanners are resolved.
"""

from collections import Counter
from pathlib import Path


def parse_scanners(text: str) -> list[list[tuple[int, int, int]]]:
    """Parse scanner blocks into a list of beacon-coordinate lists."""
    scanners: list[list[tuple[int, int, int]]] = []
    for block in text.strip().split("\n\n"):
        beacons: list[tuple[int, int, int]] = []
        for line in block.splitlines()[1:]:
            parts = line.split(",")
            if len(parts) == 3:
                beacons.append((int(parts[0]), int(parts[1]), int(parts[2])))
        scanners.append(beacons)
    return scanners


def all_rotations(point: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    """Return all 24 orientations of a 3-D *point*.

    The 24 rotation matrices of the cube symmetry group are enumerated
    explicitly (6 face choices x 4 in-face rotations).
    """
    x, y, z = point
    return [
        (x, y, z), (x, -z, y), (x, -y, -z), (x, z, -y),
        (-x, -y, z), (-x, z, y), (-x, y, -z), (-x, -z, -y),
        (y, z, x), (y, -x, z), (y, -z, -x), (y, x, -z),
        (-y, -z, x), (-y, x, z), (-y, z, -x), (-y, -x, -z),
        (z, x, y), (z, -y, x), (z, -x, -y), (z, y, -x),
        (-z, -x, y), (-z, y, x), (-z, x, -y), (-z, -y, -x),
    ]


def _rotate_beacons(
    beacons: list[tuple[int, int, int]], rot_idx: int,
) -> list[tuple[int, int, int]]:
    """Rotate every beacon by the rotation at index *rot_idx*."""
    return [all_rotations(b)[rot_idx] for b in beacons]


def _try_match(
    resolved_beacons: set[tuple[int, int, int]],
    candidate: list[tuple[int, int, int]],
) -> tuple[tuple[int, int, int], list[tuple[int, int, int]]] | None:
    """Try all 24 rotations of *candidate* against *resolved_beacons*.

    Returns (offset, transformed_beacons) if >= 12 beacons align, else None.
    """
    for rot_idx in range(24):
        rotated = _rotate_beacons(candidate, rot_idx)
        offsets: Counter[tuple[int, int, int]] = Counter()
        for rx, ry, rz in resolved_beacons:
            for cx, cy, cz in rotated:
                offsets[(rx - cx, ry - cy, rz - cz)] += 1
        for offset, count in offsets.items():
            if count >= 12:
                dx, dy, dz = offset
                translated = [(cx + dx, cy + dy, cz + dz) for cx, cy, cz in rotated]
                return offset, translated
    return None


def align_scanners(
    scanners: list[list[tuple[int, int, int]]],
) -> tuple[set[tuple[int, int, int]], list[tuple[int, int, int]]]:
    """Align all scanners to scanner 0's frame.

    Returns (all_beacons, scanner_positions).
    """
    resolved_beacons: dict[int, set[tuple[int, int, int]]] = {
        0: set(scanners[0]),
    }
    scanner_positions: dict[int, tuple[int, int, int]] = {0: (0, 0, 0)}
    queue = [0]
    unresolved = set(range(1, len(scanners)))

    while queue:
        current = queue.pop(0)
        for idx in list(unresolved):
            result = _try_match(resolved_beacons[current], scanners[idx])
            if result is not None:
                offset, translated = result
                resolved_beacons[idx] = set(translated)
                scanner_positions[idx] = offset
                unresolved.discard(idx)
                queue.append(idx)

    if unresolved:
        raise RuntimeError(f"Could not resolve scanners: {unresolved}")

    all_beacons: set[tuple[int, int, int]] = set()
    for beacons in resolved_beacons.values():
        all_beacons.update(beacons)

    return all_beacons, list(scanner_positions.values())


def solve(input_path: str = "advent2021/Day19/d19_input.txt") -> int:
    """Read scanner data, align all scanners, and return the beacon count."""
    text = Path(input_path).read_text()
    scanners = parse_scanners(text)
    beacons, _ = align_scanners(scanners)
    return len(beacons)


if __name__ == "__main__":
    result = solve()
    print(f"Total unique beacons: {result}")
