#!/usr/bin/env python3
"""Advent of Code 2016 Day 4 Part 2: find northpole object storage."""

from collections import Counter
from pathlib import Path
import re


PAT = re.compile(r"^([a-z-]+)-(\d+)\[([a-z]+)\]$")


def is_real(name: str, checksum: str) -> bool:
    """Return whether the room checksum is valid."""
    counts = Counter(ch for ch in name if ch != "-")
    want = "".join(sorted(counts, key=lambda ch: (-counts[ch], ch))[:5])
    return want == checksum


def decrypt(name: str, shift: int) -> str:
    """Caesar-shift dashed room name by sector ID."""
    out: list[str] = []
    k = shift % 26
    for ch in name:
        if ch == "-":
            out.append(" ")
        else:
            out.append(chr((ord(ch) - 97 + k) % 26 + 97))
    return "".join(out)


def solve(s: str) -> int:
    """Return sector ID for room decrypting to northpole object storage."""
    for line in s.splitlines():
        m = PAT.match(line.strip())
        if not m:
            continue
        name, sid, chk = m.group(1), int(m.group(2)), m.group(3)
        if is_real(name, chk):
            plain = decrypt(name, sid)
            if "northpole" in plain and "object" in plain:
                return sid
    raise ValueError("northpole object storage not found")


if __name__ == "__main__":
    text = Path(__file__).with_name("d4_input.txt").read_text(encoding="utf-8")
    print(solve(text))
