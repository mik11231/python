"""HTTP wrappers for Advent of Code requests with consistent headers/timeouts."""

from __future__ import annotations

import requests


def _headers(user_agent: str, session_cookie: str | None = None) -> dict[str, str]:
    """
    Run `_headers` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: user_agent, session_cookie.
    - Returns the computed result for this stage of the pipeline.
    """
    headers = {"User-Agent": user_agent}
    if session_cookie:
        headers["Cookie"] = f"session={session_cookie}"
    return headers


def aoc_get(url: str, user_agent: str, session_cookie: str | None = None, timeout: int = 30) -> requests.Response:
    """Issue a GET request to AoC with standardized headers."""
    return requests.get(url, headers=_headers(user_agent, session_cookie), timeout=timeout)


def aoc_post(
    url: str,
    user_agent: str,
    data: dict[str, str],
    session_cookie: str,
    timeout: int = 30,
) -> requests.Response:
    """Issue a POST request to AoC with standardized headers."""
    return requests.post(url, headers=_headers(user_agent, session_cookie), data=data, timeout=timeout)
