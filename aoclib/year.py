"""Year inference utilities for Advent of Code projects."""

from __future__ import annotations

from pathlib import Path


def infer_default_year(fallback: int = 2025, cwd: Path | None = None) -> int:
    """Infer Advent of Code year from cwd path segments, with fallback."""
    base = cwd if cwd is not None else Path.cwd()
    for part in reversed(base.parts):
        tokens = part.replace("-", " ").replace("_", " ").split()
        for token in tokens:
            if token.isdigit():
                year = int(token)
                if 2015 <= year <= 2100:
                    return year
    return fallback
