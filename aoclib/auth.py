"""Authentication helpers for Advent of Code scripts."""

from __future__ import annotations

import base64
from pathlib import Path


def load_session_cookie(root: Path | None = None) -> str:
    """Load and decode `.aoc_session_b64` from the repository root.

    Returns an empty string when the file is missing/invalid.
    """
    base = root if root is not None else Path(__file__).resolve().parents[1]
    path = base / ".aoc_session_b64"
    if not path.is_file():
        return ""

    data = path.read_text(encoding="utf-8").strip()
    if not data:
        return ""

    try:
        decoded = base64.b64decode(data.encode("utf-8")).decode("utf-8").strip()
    except Exception:
        return ""
    return decoded


def encode_session_cookie(cookie: str) -> str:
    """Return base64-encoded representation of a raw AoC session cookie."""
    return base64.b64encode(cookie.encode("utf-8")).decode("ascii")
