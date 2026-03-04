"""Parsing helpers commonly used in Advent of Code solutions."""

from __future__ import annotations

import re
from typing import Iterable


def ints(text: str) -> list[int]:
    """Extract all signed integers from text."""
    return [int(x) for x in re.findall(r"-?\d+", text)]


def lines(text: str, keep_blank: bool = False) -> list[str]:
    """Split text into lines, optionally dropping empty lines."""
    out = text.splitlines()
    if keep_blank:
        return out
    return [line for line in out if line.strip()]


def blocks(text: str) -> list[list[str]]:
    """Split input into blank-line separated blocks of stripped lines."""
    out: list[list[str]] = []
    current: list[str] = []
    for raw in text.splitlines():
        line = raw.strip("\n")
        if line.strip() == "":
            if current:
                out.append(current)
                current = []
            continue
        current.append(line)
    if current:
        out.append(current)
    return out


def comma_ints(text: str) -> list[int]:
    """Parse comma-separated integers with optional spaces."""
    return [int(part.strip()) for part in text.split(",") if part.strip()]


def as_grid(lines_iter: Iterable[str]) -> list[list[str]]:
    """Convert iterable of strings into a list-of-lists character grid."""
    return [list(line.rstrip("\n")) for line in lines_iter]
