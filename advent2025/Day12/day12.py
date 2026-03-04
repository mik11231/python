#!/usr/bin/env python3
"""Advent of Code 2025 - Day 12: Christmas Tree Farm (Part 1)."""

from __future__ import annotations
from pathlib import Path

import re
from functools import lru_cache


def _norm(cells: set[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    """
    Run `_norm` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: cells.
    - Returns the computed result for this stage of the pipeline.
    """
    min_r = min(r for r, _ in cells)
    min_c = min(c for _, c in cells)
    shifted = sorted((r - min_r, c - min_c) for r, c in cells)
    return tuple(shifted)


def _transform(cells: set[tuple[int, int]], op: int) -> set[tuple[int, int]]:
    """
    Run `_transform` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: cells, op.
    - Returns the computed result for this stage of the pipeline.
    """
    out: set[tuple[int, int]] = set()
    for r, c in cells:
        x, y = r, c
        if op & 1:
            y = -y
        if op & 2:
            x = -x
        if op & 4:
            x, y = y, x
        out.add((x, y))
    return out


def all_variants(cells: set[tuple[int, int]]) -> list[tuple[tuple[int, int], int, int, int]]:
    """
    Return unique rotations/reflections as (coords, h, w, area).
    coords are normalized to start at (0, 0).
    """
    seen: set[tuple[tuple[int, int], ...]] = set()
    out: list[tuple[tuple[int, int], int, int, int]] = []
    for op in range(8):
        cs = _norm(_transform(cells, op))
        if cs in seen:
            continue
        seen.add(cs)
        h = max(r for r, _ in cs) + 1
        w = max(c for _, c in cs) + 1
        out.append((cs, h, w, len(cs)))
    return out


def parse_input(path: Path) -> tuple[list[set[tuple[int, int]]], list[tuple[int, int, list[int]]]]:
    """
    Run `parse_input` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: path.
    - Returns the computed result for this stage of the pipeline.
    """
    lines = path.read_text(encoding="utf-8").splitlines()

    shapes: dict[int, list[str]] = {}
    regions: list[tuple[int, int, list[int]]] = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        m_shape = re.match(r"^(\d+):$", line)
        if m_shape:
            idx = int(m_shape.group(1))
            i += 1
            rows: list[str] = []
            while i < len(lines):
                nxt = lines[i].strip()
                if not nxt:
                    break
                if re.match(r"^\d+:$", nxt) or re.match(r"^\d+x\d+:", nxt):
                    break
                rows.append(nxt)
                i += 1
            shapes[idx] = rows
            continue

        m_region = re.match(r"^(\d+)x(\d+):\s*(.*)$", line)
        if m_region:
            w = int(m_region.group(1))
            h = int(m_region.group(2))
            counts = list(map(int, m_region.group(3).split())) if m_region.group(3).strip() else []
            regions.append((w, h, counts))
            i += 1
            continue

        i += 1

    if not shapes:
        raise ValueError("No shapes found in input")

    max_idx = max(shapes)
    ordered: list[set[tuple[int, int]]] = []
    for idx in range(max_idx + 1):
        rows = shapes.get(idx)
        if rows is None:
            raise ValueError(f"Missing shape index {idx}")
        cells = {(r, c) for r, row in enumerate(rows) for c, ch in enumerate(row) if ch == "#"}
        if not cells:
            raise ValueError(f"Shape {idx} has no filled cells")
        ordered.append(cells)

    return ordered, regions


def can_fit_exact(
    w: int,
    h: int,
    counts: list[int],
    shape_variants: list[list[tuple[tuple[int, int], int, int, int]]],
    shape_areas: list[int],
) -> bool:
    """Exact set-packing solver for dense/small instances."""
    n_shapes = len(shape_variants)
    if len(counts) != n_shapes:
        return False

    board_area = w * h
    demand = sum(counts[i] * shape_areas[i] for i in range(n_shapes))
    if demand > board_area:
        return False

    if sum(counts) == 0:
        return True

    # Fast guaranteed fit: reserve one disjoint 3x3 box per present.
    # Works when all shapes fit in 3x3 (true for this puzzle input).
    if all(max(v[1], v[2]) <= 3 for vs in shape_variants for v in vs):
        if sum(counts) <= (w // 3) * (h // 3):
            return True

    placements_by_shape: list[list[int]] = [[] for _ in range(n_shapes)]
    for si, variants in enumerate(shape_variants):
        for coords, ph, pw, _ in variants:
            for r0 in range(h - ph + 1):
                base = r0 * w
                for c0 in range(w - pw + 1):
                    mask = 0
                    for dr, dc in coords:
                        bit = (base + dr * w + c0 + dc)
                        mask |= 1 << bit
                    placements_by_shape[si].append(mask)

    total_cells = board_area
    full_mask = (1 << total_cells) - 1

    @lru_cache(maxsize=None)
    def dfs(remaining: tuple[int, ...], occ_mask: int, rem_area: int) -> bool:
        """
        Run `dfs` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: remaining, occ_mask, rem_area.
        - Returns the computed result for this stage of the pipeline.
        """
        if rem_area == 0:
            return True

        free_cells = total_cells - occ_mask.bit_count()
        if rem_area > free_cells:
            return False

        best_si = -1
        best_opts: list[int] | None = None
        best_count = 10**18
        for si, need in enumerate(remaining):
            if need == 0:
                continue
            opts = [pm for pm in placements_by_shape[si] if (pm & occ_mask) == 0]
            if not opts:
                return False
            if len(opts) < best_count:
                best_count = len(opts)
                best_opts = opts
                best_si = si

        assert best_opts is not None and best_si >= 0

        rem_list = list(remaining)
        rem_list[best_si] -= 1
        next_remaining = tuple(rem_list)
        next_area = rem_area - shape_areas[best_si]

        for pm in best_opts:
            if dfs(next_remaining, occ_mask | pm, next_area):
                return True
        return False

    return dfs(tuple(counts), 0, demand)


def solve() -> int:
    """Count regions that can fit all requested presents."""
    shapes, regions = parse_input(Path(__file__).with_name('d12_input.txt'))
    variants = [all_variants(s) for s in shapes]
    areas = [len(s) for s in shapes]

    total = 0
    for w, h, counts in regions:
        if can_fit_exact(w, h, counts, variants, areas):
            total += 1
    return total


if __name__ == "__main__":
    ans = solve()
    print(f"Regions that can fit all presents: {ans}")
