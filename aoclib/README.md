# aoclib

Shared, dependency-light utility library for Advent of Code solutions and repo
scripts. The goal is to avoid re-implementing parsing/search/geometry/tooling
primitives across years.

## Design goals

- Keep APIs small and composable
- Prefer pure-Python helpers that work across years
- Be explicit about assumptions (inclusive ranges, Manhattan conventions, etc.)
- Support both puzzle solutions and operational tooling

## Modules and APIs

## `aoclib.auth`

Authentication/session helpers.

- `load_session_cookie(root: Path | None = None) -> str`
  - Reads `.aoc_session_b64` under `root` (defaults to repo root)
  - Returns decoded cookie or empty string if file is missing/invalid
- `encode_session_cookie(cookie: str) -> str`
  - Base64-encodes a raw cookie for storage in `.aoc_session_b64`

Typical usage:

```python
from pathlib import Path
from aoclib.auth import load_session_cookie

cookie = load_session_cookie(root=Path('.'))
```

## `aoclib.year`

Year inference helpers.

- `infer_default_year(fallback: int = 2025, cwd: Path | None = None) -> int`
  - Scans cwd path parts for a plausible 4-digit year token
  - Returns `fallback` when inference fails

## `aoclib.http`

Thin request wrappers with uniform header/cookie behavior.

- `aoc_get(url, user_agent, session_cookie=None, timeout=30) -> requests.Response`
- `aoc_post(url, user_agent, data, session_cookie, timeout=30) -> requests.Response`

These wrappers centralize AoC request conventions used by `tools/` scripts.

## `aoclib.parsing`

General-purpose input parsers.

- `ints(text) -> list[int]`
  - Extract signed integers via regex
- `lines(text, keep_blank=False) -> list[str]`
  - Split text into lines, optionally preserving blank lines
- `blocks(text) -> list[list[str]]`
  - Split into blank-line-separated groups of lines
- `comma_ints(text) -> list[int]`
  - Parse comma-separated integers with optional spaces
- `as_grid(lines_iter) -> list[list[str]]`
  - Convert lines to char grid

## `aoclib.grid`

2D grid helpers.

Constants:

- `DIR4`: cardinal deltas
- `DIR8`: cardinal + diagonal deltas

Functions:

- `in_bounds(r, c, rows, cols) -> bool`
- `neighbors4(r, c, rows, cols) -> Iterator[(r, c)]`
- `neighbors8(r, c, rows, cols) -> Iterator[(r, c)]`
- `find_cells(grid, target) -> list[(r, c)]`
- `to_lines(grid) -> list[str]`

## `aoclib.search`

Graph shortest-path helpers.

- `bfs_distances(start, neighbors) -> dict[node, int]`
  - Unweighted shortest distances from `start`
- `dijkstra_distances(start, neighbors) -> dict[node, int]`
  - Weighted non-negative shortest distances
  - `neighbors(node)` must yield `(next_node, edge_cost)` pairs

Used directly in several day solutions after standardization passes.

## `aoclib.runner`

Execution helpers for standard day-script I/O patterns.

- `read_input_for(script_file, input_name) -> str`
  - Reads an input file located next to a day script.
- `print_answer(answer, label=None) -> None`
  - Prints answer in a consistent way, optionally prefixed by a label.

## `aoclib.geometry`

Distance helpers.

- `manhattan2((x1, y1), (x2, y2)) -> int`
- `manhattan3((x1, y1, z1), (x2, y2, z2)) -> int`

## `aoclib.intervals`

Inclusive interval operations.

- `merge_intervals(intervals, touch=True) -> list[(lo, hi)]`
  - Merges overlaps; with `touch=True`, adjacent intervals also merge
- `covered_length(intervals, touch=True) -> int`
  - Total covered integer points for inclusive ranges
- `clamp_interval((a, b), lo, hi) -> (a', b') | None`
- `first_gap(intervals, lo, hi) -> int | None`
  - First uncovered integer in `[lo, hi]`
- `contains_interval(container, containee) -> bool`
- `intervals_overlap(a, b, touch=True) -> bool`
- `parse_int_range('start-end') -> (start, end)`

## Where it is used

- All repo tool scripts in `tools/` import `aoclib.auth/year/http`
- Multiple year/day solutions now import `aoclib.grid/search/geometry/intervals`
  after consistency and deduplication passes

## Import patterns for day scripts

When running day scripts directly by file path, ensure repo root is importable:

```python
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
```

This pattern is used in refactored day files that import `aoclib` from nested
`advent20XX/DayN/` paths.
