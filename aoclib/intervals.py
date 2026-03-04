"""Interval helpers for range-union and gap scanning problems."""

from __future__ import annotations


def merge_intervals(intervals: list[tuple[int, int]], *, touch: bool = True) -> list[tuple[int, int]]:
    """Merge sorted/unsorted inclusive intervals.

    When `touch=True`, adjacent intervals like [1,3] and [4,5] are merged.
    """
    if not intervals:
        return []

    sorted_intervals = sorted(intervals)
    merged: list[tuple[int, int]] = [sorted_intervals[0]]
    for a, b in sorted_intervals[1:]:
        ma, mb = merged[-1]
        limit = mb + 1 if touch else mb
        if a > limit:
            merged.append((a, b))
        else:
            merged[-1] = (ma, max(mb, b))
    return merged


def covered_length(intervals: list[tuple[int, int]], *, touch: bool = True) -> int:
    """Return total covered cell count for inclusive intervals."""
    return sum(b - a + 1 for a, b in merge_intervals(intervals, touch=touch))


def clamp_interval(interval: tuple[int, int], lo: int, hi: int) -> tuple[int, int] | None:
    """Clamp inclusive interval to [lo, hi], or return None if empty."""
    a, b = interval
    a = max(a, lo)
    b = min(b, hi)
    if a > b:
        return None
    return a, b


def first_gap(intervals: list[tuple[int, int]], lo: int, hi: int) -> int | None:
    """Return the first uncovered x in [lo, hi] for inclusive intervals."""
    x = lo
    for a, b in merge_intervals(intervals, touch=True):
        if a > x:
            return x
        x = max(x, b + 1)
        if x > hi:
            return None
    return x if x <= hi else None


def contains_interval(container: tuple[int, int], containee: tuple[int, int]) -> bool:
    """Return True when `container` fully covers `containee` (inclusive)."""
    a1, a2 = container
    b1, b2 = containee
    return a1 <= b1 and a2 >= b2


def intervals_overlap(a: tuple[int, int], b: tuple[int, int], *, touch: bool = True) -> bool:
    """Return True when intervals overlap (or touch, when enabled)."""
    a1, a2 = a
    b1, b2 = b
    if touch:
        return not (a2 < b1 or b2 < a1)
    return not (a2 <= b1 or b2 <= a1)


def parse_int_range(text: str, sep: str = "-") -> tuple[int, int]:
    """Parse `start-end` into an inclusive integer interval tuple."""
    start, end = map(int, text.split(sep))
    return start, end
