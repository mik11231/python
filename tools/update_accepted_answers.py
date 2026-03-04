#!/usr/bin/env python3
"""Regenerate tools/accepted_answers.json from advent year README files."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).with_name("accepted_answers.json")


def build_answers() -> dict[str, dict[str, dict[str, str]]]:
    data: dict[str, dict[str, dict[str, str]]] = {}
    pattern = re.compile(
        r"- Day\s+(\d+):\s+Part\s+1\s*=\s*`([^`]*)`(?:,\s*Part\s*2\s*=\s*`([^`]*)`)?"
    )

    for readme in sorted(ROOT.glob("advent20*/README.md")):
        year = readme.parent.name.replace("advent", "")
        text = readme.read_text(encoding="utf-8")
        days: dict[str, dict[str, str]] = {}
        for m in pattern.finditer(text):
            day = str(int(m.group(1)))
            p1 = m.group(2)
            p2 = m.group(3)
            parts = {"1": p1}
            if p2 is not None:
                parts["2"] = p2
            days[day] = parts
        if days:
            data[year] = days

    return data


def main() -> int:
    data = build_answers()
    OUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} (years: {', '.join(sorted(data.keys()))})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
