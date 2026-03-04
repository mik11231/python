#!/usr/bin/env python3
"""
Helper script to store your Advent of Code session cookie in base64 form.

Usage (from repo root):

    python tools/encode_aoc_session.py

You will be prompted for the cookie; it will NOT be echoed back.
The script writes `.aoc_session_b64` in the repo root, which is already
ignored by git (see .gitignore).
"""

import getpass
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aoclib.auth import encode_session_cookie


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

    encoded = encode_session_cookie(cookie)

    out_path = Path(".aoc_session_b64")
    out_path.write_text(encoded + "\n", encoding="utf-8")
    print(f"Wrote base64-encoded cookie to {out_path} (git-ignored).")


if __name__ == "__main__":
    main()

