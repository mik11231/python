#!/usr/bin/env python3
"""
Advent of Code answer submitter.

Usage:
    python tools/submit_answer.py <day> <part> <answer> [year]

Example:
    python tools/submit_answer.py 12 1 408
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import requests

from aoclib.http import aoc_post
from aoclib.year import infer_default_year
try:
    from tools.download_input import get_session_cookie
except ImportError:
    from download_input import get_session_cookie


def submit_answer(year: int, day: int, part: int, answer: str, session_cookie: str) -> bool:
    """Submit an AoC answer and return True when accepted as correct."""
    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    user_agent = "Mozilla/5.0 (compatible; AOC-Answer-Submitter/1.0)"
    data = {"level": str(part), "answer": str(answer)}

    print(f"Submitting answer for Day {day} Part {part}, Year {year}...")
    print(f"URL: {url}")

    try:
        response = aoc_post(
            url=url,
            user_agent=user_agent,
            data=data,
            session_cookie=session_cookie,
            timeout=30,
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out after 30 seconds")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"[ERROR] Connection error: {e}")
        return False
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else "unknown"
        print(f"[ERROR] HTTP error {status}: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

    text = response.text

    if "That's the right answer!" in text:
        print("[OK] That's the right answer!")
        return True

    if "Did you already complete it?" in text:
        print("[INFO] This part appears to be already completed.")
        return True

    if "That's not the right answer." in text:
        print("[INFO] That's not the right answer.")
        wait_match = re.search(r"You have (.+?) left to wait", text)
        if wait_match:
            print(f"[INFO] Rate limit status: wait {wait_match.group(1)}.")
        return False

    if "You gave an answer too recently" in text:
        print("[INFO] You gave an answer too recently; wait before trying again.")
        wait_match = re.search(r"You have (.+?) left to wait", text)
        if wait_match:
            print(f"[INFO] Remaining wait: {wait_match.group(1)}.")
        return False

    # Fallback: print the first article snippet if present.
    m = re.search(r"<article>(.*?)</article>", text, flags=re.DOTALL)
    if m:
        snippet = re.sub(r"<[^>]+>", " ", m.group(1))
        snippet = " ".join(snippet.split())
        print(f"[INFO] Server response: {snippet[:300]}")
    else:
        print("[INFO] Received response, but no known outcome marker was found.")

    return False


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
    session_cookie = get_session_cookie()
    default_year = infer_default_year(2025)

    if len(sys.argv) < 4:
        print("Usage: python tools/submit_answer.py <day> <part> <answer> [year]")
        print(f"  Default year (if omitted): {default_year}")
        print("  Example: python tools/submit_answer.py 12 1 408")
        if session_cookie:
            print("\n[OK] Session cookie found in .aoc_session_b64.")
        else:
            print("\nYou must create `.aoc_session_b64` in the repo root containing")
            print("a base64-encoded Advent of Code session cookie.")
        sys.exit(1)

    try:
        day = int(sys.argv[1])
        part = int(sys.argv[2])
        answer = sys.argv[3]
        year = int(sys.argv[4]) if len(sys.argv) >= 5 else default_year
    except ValueError:
        print("Error: day, part, and year must be integers (answer can be any token/string).")
        sys.exit(1)

    if not (1 <= day <= 25):
        print("Error: Day must be between 1 and 25")
        sys.exit(1)
    if part not in (1, 2):
        print("Error: Part must be 1 or 2")
        sys.exit(1)

    if not session_cookie:
        print("Error: No session cookie found in .aoc_session_b64")
        sys.exit(1)
    if len(session_cookie) < 10:
        print("Error: Session cookie appears invalid (too short)")
        sys.exit(1)

    ok = submit_answer(year, day, part, answer, session_cookie)
    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()
