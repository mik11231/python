"""Shared utilities for Advent of Code tooling in this repository."""

from .auth import encode_session_cookie, load_session_cookie
from .geometry import manhattan2, manhattan3
from .http import aoc_get, aoc_post
from .intervals import (
    clamp_interval,
    contains_interval,
    covered_length,
    first_gap,
    intervals_overlap,
    merge_intervals,
    parse_int_range,
)
from .parsing import as_grid, blocks, comma_ints, ints, lines
from .runner import print_answer, read_input_for
from .search import bfs_distances, dijkstra_distances
from .year import infer_default_year

__all__ = [
    "encode_session_cookie",
    "load_session_cookie",
    "infer_default_year",
    "aoc_get",
    "aoc_post",
    "ints",
    "lines",
    "blocks",
    "comma_ints",
    "as_grid",
    "read_input_for",
    "print_answer",
    "bfs_distances",
    "dijkstra_distances",
    "manhattan2",
    "manhattan3",
    "merge_intervals",
    "covered_length",
    "clamp_interval",
    "first_gap",
    "contains_interval",
    "intervals_overlap",
    "parse_int_range",
]
