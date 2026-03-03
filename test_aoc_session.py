#!/usr/bin/env python3
"""
Quick helper to verify that `.aoc_session_b64` contains a working AoC session.

It:
- reads the base64-encoded cookie from `.aoc_session_b64` in the repo root,
- decodes it,
- makes a single authenticated request to your Day 1 input,
- prints the cookie length and HTTP status code (but never the cookie itself).
"""

import base64
from pathlib import Path

import requests


def load_cookie_from_b64() -> str:
    path = Path(".aoc_session_b64")
    if not path.is_file():
        raise FileNotFoundError(".aoc_session_b64 not found in repo root")
    data = path.read_text(encoding="utf-8").strip()
    if not data:
        raise ValueError(".aoc_session_b64 is empty")
    raw = base64.b64decode(data.encode("utf-8")).decode("utf-8")
    return raw.strip()


def main() -> None:
    cookie = load_cookie_from_b64()
    print(f"Decoded cookie length: {len(cookie)} characters")

    url = "https://adventofcode.com/2025/day/1/input"
    headers = {
        "Cookie": f"session={cookie}",
        "User-Agent": "AoC-Session-Tester/1.0 (+github.com/mik11231/aoc2025)",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=15)
    except Exception as e:
        print(f"Request failed: {e}")
        return

    print(f"HTTP status: {resp.status_code}")
    if resp.status_code == 200:
        print("Session token appears to be VALID (received HTTP 200).")
    elif resp.status_code == 400:
        print("Server returned 400 Bad Request – this often indicates an invalid/expired session.")
    elif resp.status_code == 404:
        print("Got 404 – maybe Day 1 input is not available yet?")
    else:
        print("Non-200 status; token might be invalid or there may be another issue.")


if __name__ == "__main__":
    main()

