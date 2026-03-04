#!/usr/bin/env python3
"""
Advent of Code Instructions Downloader

This script downloads the puzzle instructions page (HTML) from adventofcode.com
for a given year/day.

If a session cookie is available (via `.aoc_session_b64` in the repo root),
it will be sent with the request; otherwise the request is anonymous. For
released days, instructions are usually public, so the cookie is optional.
"""

import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aoclib.http import aoc_get
from aoclib.year import infer_default_year
try:
    from tools.download_input import get_session_cookie
except ImportError:
    from download_input import get_session_cookie


def download_instructions(year, day, session_cookie=None, output_dir=None, verbose=True):
    """
    Download puzzle instructions (HTML) for a specific day.

    Args:
        year: Year (e.g., 2025)
        day: Day number (1-25)
        session_cookie: Your AOC session cookie (optional for public days)
        output_dir: Directory to save the file (default: Day{day}/)

    Returns:
        Path to downloaded file, or None if failed

    The file will be saved to: Day{day}/d{day}_instructions.html
    Example: Day6/d6_instructions.html
    """
    url = f"https://adventofcode.com/{year}/day/{day}"

    user_agent = "Mozilla/5.0 (compatible; AOC-Instructions-Downloader/1.0)"

    try:
        if verbose:
            print(f"Downloading instructions for Day {day}, Year {year}...")
            print(f"URL: {url}")
        response = aoc_get(
            url=url,
            user_agent=user_agent,
            session_cookie=session_cookie,
            timeout=30,
        )
        response.raise_for_status()
        if verbose:
            print(f"[OK] Successfully downloaded {len(response.text)} characters of instructions")

        # Always use Day{day} folder format
        if output_dir is None:
            output_dir = Path(f"Day{day}")
        else:
            output_dir = Path(output_dir)

        output_dir.mkdir(parents=True, exist_ok=True)

        # Save full HTML so it can be opened in a browser
        output_file = output_dir / f"d{day}_instructions.html"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(response.text)

        print(f"[OK] Downloaded instructions for Day {day} to {output_file}")
        return output_file

    except requests.exceptions.Timeout:
        print(f"[ERROR] Request timed out after 30 seconds while downloading instructions")
        print("  Check your internet connection and try again")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"[ERROR] Connection error while downloading instructions: {e}")
        print("  Check your internet connection")
        return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"[ERROR] Day {day} instructions not available yet (404)")
        elif e.response.status_code == 400:
            print(f"[ERROR] Bad request - check your session cookie")
        elif e.response.status_code == 500:
            print(f"[ERROR] Server error (500) - Advent of Code might be down")
        else:
            print(f"[ERROR] HTTP Error {e.response.status_code}: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Error downloading instructions: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main function to handle command line usage."""
    # Optional session cookie from .aoc_session_b64
    session_cookie = get_session_cookie()

    DEFAULT_YEAR = infer_default_year(2025)

    if len(sys.argv) < 2:
        print("Usage: python tools/download_instructions.py <day> [year] [base_dir]")
        print(f"  Default year (if omitted): {DEFAULT_YEAR}")
        print("  Output: <base_dir>/Day<day>/d<day>_instructions.html (base_dir defaults to .)")
        if session_cookie:
            print("\n[OK] Session cookie found in .aoc_session_b64 (optional for instructions).")
        else:
            print("\nTo add an optional session cookie, create `.aoc_session_b64`")
            print("in the repo root with your base64-encoded AoC session token.")
        sys.exit(1)

    day = int(sys.argv[1])

    # Year: either provided explicitly or inferred from project path
    if len(sys.argv) >= 3:
        year = int(sys.argv[2])
    else:
        year = DEFAULT_YEAR
    base_dir = Path(sys.argv[3]) if len(sys.argv) >= 4 else Path(".")

    if not (1 <= day <= 25):
        print("Error: Day must be between 1 and 25")
        sys.exit(1)

    download_instructions(
        year,
        day,
        session_cookie=session_cookie,
        output_dir=base_dir / f"Day{day}",
    )


if __name__ == "__main__":
    main()

