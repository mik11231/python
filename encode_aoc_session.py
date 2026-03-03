#!/usr/bin/env python3
"""
Helper script to store your Advent of Code session cookie in base64 form.

Usage (from repo root):

    python encode_aoc_session.py

You will be prompted for the cookie; it will NOT be echoed back.
The script writes `.aoc_session_b64` in the repo root, which is already
ignored by git (see .gitignore).
"""

import base64
import getpass
from pathlib import Path


def main() -> None:
    cookie = getpass.getpass("Enter your Advent of Code session cookie: ").strip()
    if not cookie:
        print("No cookie entered, aborting.")
        return

    # AoC session cookies are typically fairly long; add a sanity check so we
    # don't accidentally encode a truncated value.
    length = len(cookie)
    print(f"Cookie length: {length} characters.")
    if length < 40:
        resp = input(
            "Warning: this looks shorter than a typical AoC session cookie. "
            "Are you sure it's complete? [y/N]: "
        ).strip().lower()
        if resp not in ("y", "yes"):
            print("Aborting without writing .aoc_session_b64.")
            return

    encoded = base64.b64encode(cookie.encode("utf-8")).decode("ascii")

    out_path = Path(".aoc_session_b64")
    out_path.write_text(encoded + "\n", encoding="utf-8")
    print(f"Wrote base64-encoded cookie to {out_path} (git-ignored).")


if __name__ == "__main__":
    main()

