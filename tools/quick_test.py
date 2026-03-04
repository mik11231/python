#!/usr/bin/env python3
"""Quick end-to-end connectivity check for Advent of Code tooling."""

import requests
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aoclib.http import aoc_get
try:
    from tools.download_input import get_session_cookie, infer_default_year
except ImportError:
    from download_input import get_session_cookie, infer_default_year


def main() -> None:
    """Validate cookie loading and perform one authenticated AoC request."""
    cookie = get_session_cookie()
    if not cookie:
        print("[ERROR] No session cookie found in .aoc_session_b64")
        print("Run: python tools/encode_aoc_session.py")
        raise SystemExit(1)

    year = infer_default_year(2025)
    url = f"https://adventofcode.com/{year}/day/1/input"
    user_agent = "Mozilla/5.0 (compatible; AOC-Quick-Test/1.0)"

    print(f"[OK] Loaded session cookie from .aoc_session_b64 (length: {len(cookie)})")
    print(f"Testing authenticated request: {url}")

    try:
        resp = aoc_get(url=url, user_agent=user_agent, session_cookie=cookie, timeout=15)
    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out after 15 seconds")
        raise SystemExit(2)
    except requests.exceptions.ConnectionError as e:
        print(f"[ERROR] Connection error: {e}")
        raise SystemExit(2)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        raise SystemExit(2)

    print(f"HTTP status: {resp.status_code}")
    if resp.status_code == 200:
        print(f"[OK] Authenticated request worked ({len(resp.text)} characters returned).")
        return
    if resp.status_code == 400:
        print("[INFO] 400 Bad Request: session cookie is likely invalid or expired.")
    elif resp.status_code == 404:
        print("[INFO] 404 Not Found: day/input may not be unlocked yet for that year.")
    else:
        print("[INFO] Non-200 response received; check cookie validity and account state.")
    raise SystemExit(3)


if __name__ == "__main__":
    main()
