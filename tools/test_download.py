#!/usr/bin/env python3
"""Quick test script to debug download issues and cookie setup."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aoclib.http import aoc_get
try:
    from tools.download_input import get_session_cookie
except ImportError:
    from download_input import get_session_cookie

print("=== Cookie file check ===")
cookie = get_session_cookie()
if cookie:
    print(f"[OK] .aoc_session_b64 found and decoded (length: {len(cookie)})")
    print(f"  First 10 chars: {cookie[:10]}...")
else:
    print("[X] No valid cookie found in .aoc_session_b64")
    print("\nRun tools/encode_aoc_session.py to create/update it.")

print("\n=== Testing requests library ===")
print("[OK] requests library is installed")
try:
    # Test a simple request
    print("\nTesting network connection...")
    response = aoc_get(
        url="https://adventofcode.com",
        user_agent="AOC-Test-Download/1.0",
        timeout=10,
    )
    print(f"[OK] Can reach adventofcode.com (status: {response.status_code})")
except Exception as e:
    print(f"✗ Network error: {e}")

print("\n=== Ready to test download ===")
if cookie:
    print("You can now run: python tools/download_input.py 1")
else:
    print("Once .aoc_session_b64 is set up, run: python tools/download_input.py 1")
