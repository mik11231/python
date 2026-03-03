#!/usr/bin/env python3
"""Quick test script to debug download issues and cookie setup."""

import sys

from download_input import get_session_cookie

print("=== Cookie file check ===")
cookie = get_session_cookie()
if cookie:
    print(f"[OK] .aoc_session_b64 found and decoded (length: {len(cookie)})")
    print(f"  First 10 chars: {cookie[:10]}...")
else:
    print("[X] No valid cookie found in .aoc_session_b64")
    print("\nRun encode_aoc_session.py to create/update it.")

print("\n=== Testing requests library ===")
try:
    import requests

    print("[OK] requests library is installed")

    # Test a simple request
    print("\nTesting network connection...")
    response = requests.get("https://adventofcode.com", timeout=10)
    print(f"[OK] Can reach adventofcode.com (status: {response.status_code})")
except ImportError:
    print("[X] requests library is NOT installed")
    print("  Run: pip install requests")
except Exception as e:
    print(f"✗ Network error: {e}")

print("\n=== Ready to test download ===")
if cookie:
    print("You can now run: python download_input.py 1")
else:
    print("Once .aoc_session_b64 is set up, run: python download_input.py 1")

