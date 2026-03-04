"""Small helpers for consistent day-script execution patterns."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def read_input_for(script_file: str, input_name: str) -> str:
    """Read an input file located beside a day script."""
    return Path(script_file).with_name(input_name).read_text()


def print_answer(answer: Any, label: str | None = None) -> None:
    """Print a final answer with an optional stable label."""
    if label:
        print(f"{label}: {answer}")
    else:
        print(answer)
