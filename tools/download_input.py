#!/usr/bin/env python3
"""
Advent of Code Input Downloader

This script downloads input files from adventofcode.com.
You need to provide your session cookie for authentication.

To get your session cookie:
1. Log in to https://adventofcode.com
2. Open browser developer tools (F12)
3. Go to Application/Storage > Cookies > adventofcode.com
4. Copy the value of the 'session' cookie
"""

import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aoclib.auth import load_session_cookie
from aoclib.http import aoc_get
from aoclib.year import infer_default_year


def get_session_cookie() -> str:
    """
    Resolve the Advent of Code session cookie.

    The ONLY source is `.aoc_session_b64` in the repo root, which must contain
    a base64-encoded session cookie value.
    """
    root = Path(__file__).resolve().parents[1]
    return load_session_cookie(root=root)

def download_input(year, day, session_cookie, output_dir=None, verbose=True):
    """
    Download input file for a specific day.
    
    Args:
        year: Year (e.g., 2025)
        day: Day number (1-25)
        session_cookie: Your AOC session cookie
        output_dir: Directory to save the file (default: Day{day}/)
    
    Returns:
        Path to downloaded file, or None if failed
    
    The file will be saved to: Day{day}/d{day}_input.txt
    Example: Day6/d6_input.txt
    """
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    
    user_agent = "Mozilla/5.0 (compatible; AOC-Input-Downloader/1.0)"
    
    try:
        if verbose:
            print(f"Downloading input for Day {day}, Year {year}...")
            print(f"URL: {url}")
        response = aoc_get(
            url=url,
            user_agent=user_agent,
            session_cookie=session_cookie,
            timeout=30,
        )
        response.raise_for_status()
        if verbose:
            print(f"[OK] Successfully downloaded {len(response.text)} characters")
        
        # Always use Day{day} folder format
        if output_dir is None:
            output_dir = Path(f"Day{day}")
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Always use d{day}_input.txt filename format
        output_file = output_dir / f"d{day}_input.txt"
        
        # Save the input
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text.rstrip('\n'))
        
        print(f"[OK] Downloaded input for Day {day} to {output_file}")
        return output_file
        
    except requests.exceptions.Timeout:
        print(f"[ERROR] Request timed out after 30 seconds")
        print(f"  Check your internet connection and try again")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"[ERROR] Connection error: {e}")
        print(f"  Check your internet connection")
        return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"[ERROR] Day {day} input not available yet (404)")
        elif e.response.status_code == 400:
            print(f"[ERROR] Bad request - check your session cookie")
        elif e.response.status_code == 500:
            print(f"[ERROR] Server error (500) - Advent of Code might be down")
        else:
            print(f"[ERROR] HTTP Error {e.response.status_code}: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Error downloading input: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main function to handle command line usage."""
    # Resolve session cookie ONLY from .aoc_session_b64
    session_cookie = get_session_cookie()

    if len(sys.argv) < 2:
        print("Usage: python tools/download_input.py <day> [year] [base_dir]")
        print(f"  Default year: 2025")
        print(f"  Output: <base_dir>/Day<day>/d<day>_input.txt (base_dir defaults to .)")
        if session_cookie:
            print("\n[OK] Session cookie found in .aoc_session_b64.")
        else:
            print("\nYou must create `.aoc_session_b64` in the repo root containing")
            print("a base64-encoded Advent of Code session cookie.")
        print("\nTo get your session cookie:")
        print("1. Log in to https://adventofcode.com")
        print("2. Open browser dev tools (F12)")
        print("3. Application > Cookies > adventofcode.com > session")
        sys.exit(1)
    
    day = int(sys.argv[1])
    
    # Get session cookie from .aoc_session_b64 only
    if not session_cookie:
        print("Error: No session cookie found in .aoc_session_b64!")
        sys.exit(1)

    print(f"[OK] Using session cookie from .aoc_session_b64 (length: {len(session_cookie)})")

    if not session_cookie or len(session_cookie) < 10:
        print("Error: Session cookie appears to be invalid (too short)")
        sys.exit(1)
    
    # Get year from optional second positional arg, otherwise infer from path.
    DEFAULT_YEAR = infer_default_year(2025)
    year = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_YEAR
    base_dir = Path(sys.argv[3]) if len(sys.argv) > 3 else Path(".")
    
    if not (1 <= day <= 25):
        print("Error: Day must be between 1 and 25")
        sys.exit(1)
    
    download_input(year, day, session_cookie, output_dir=base_dir / f"Day{day}")

if __name__ == "__main__":
    main()

