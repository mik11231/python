#!/usr/bin/env python3
"""
Quick helper to verify that `.aoc_session_b64` contains a working AoC session.

It:
- reads the base64-encoded cookie from `.aoc_session_b64` in the repo root,
- decodes it,
- makes a single authenticated request to your Day 1 input,
- prints the cookie length and HTTP status code (but never the cookie itself).
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aoclib.auth import load_session_cookie
from aoclib.http import aoc_get


def load_cookie_from_b64() -> str:
    """
    Run `load_cookie_from_b64` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Returns the computed result for this stage of the pipeline.
    """
    cookie = load_session_cookie(root=Path("."))
    if not cookie:
        raise ValueError("No valid session cookie found in .aoc_session_b64")
    return cookie


def main() -> None:
    """
    Run `main` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Returns the computed result for this stage of the pipeline.
    """
    cookie = load_cookie_from_b64()
    print(f"Decoded cookie length: {len(cookie)} characters")

    url = "https://adventofcode.com/2025/day/1/input"
    user_agent = "AoC-Session-Tester/1.0 (+github.com/mik11231/aoc2025)"

    try:
        resp = aoc_get(url=url, user_agent=user_agent, session_cookie=cookie, timeout=15)
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

