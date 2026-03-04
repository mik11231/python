# Originality Check — Advent of Code Solutions

This document records a systematic check that solution code in `advent20XX/` is original and not copied from external codebases.

**Date:** 2025-03 (session)

## Scope

- All Python solution files under `advent2015/`, `advent2016/`, `advent2018/` through `advent2025/` matching `Day*/day*.py` and `Day*/day*_part2.py`.

## Checks Performed

### 1. Attribution and URLs

- **Searched for:** `http`, `github`, `reddit`, `stackoverflow`, `source:`, `adapted`, `credit`, `thanks to`, `based on`, paste/copy (in attribution sense), `inspired`, `solution by`, `solved by`, `taken from`, `credit to`, `hat tip`, `shoutout`, `kudos`, `.com`, `.org`, `.io`, `.net`, `pastebin`, `gist.github`.
- **Result:** No attribution comments or external URLs found. The only `.io` match is the puzzle title "JSAbacusFramework.io" in Day 12 2015 (problem name), not a URL.

### 2. Author / Copyright / License

- **Searched for:** `by ` (in "written by"), `author`, `written by`, `created by`, `©`, `copyright`, `license`, `GPL`, `MIT`.
- **Result:** No author, copyright, or license notices in solution files. All "by" matches are normal English in docstrings (e.g. "replace by", "multiply by", "by sitting next to").

### 3. Reddit / Social Handles

- **Searched for:** Reddit-style usernames (e.g. `u/username`).
- **Result:** None found.

### 4. “From problem” / “From input” Comments

- **Found:** Two benign comments: `# from problem` (reference to puzzle text) and `# from input:` (reference to example input). No external source attribution.

### 5. Entrypoint and Style Consistency

- **Checked:** All solution files are audited by `tools/audit_aoc.py` for a `solve` (or `solve_part1`/`solve_part2`) entrypoint and module docstrings.
- **Result:** Solutions follow the repo convention; no files use a different, single-source style that would suggest pasted code from elsewhere.

## Conclusion

No evidence was found that any solution is copied from another codebase. Checks found:

- No URLs or references to external sites (GitHub, Reddit, Stack Overflow, etc.).
- No attribution, credits, “inspired by”, or author/copyright/license text.
- No social or Reddit handles.
- Consistent use of repo patterns (`solve`, docstrings, `Path(__file__).with_name(...)` or equivalent).

## Recommendations

- Re-run this style of check after adding new years or bulk-importing solutions (e.g. `grep` for URLs and attribution in `advent*/Day*/*.py`).
- To re-run the full GitHub/snippet sweep, follow the method in **Originality Re-check (2026-03-04)** above (API pass, store results in `.local_state/originality_github_scan.json`, then triage flagged files).
- Keep using `python tools/audit_aoc.py` so all solutions retain the standard entrypoint and docstrings.

---

## Originality Re-check (2026-03-04)

### Scope

- All Python solution files under `advent*/Day*/day*.py`:
  - `473` files total (`advent2015`, `advent2016`, `advent2018`-`advent2025`).

### Method

1. **Full-repo external code-search sweep (no cloning):**
   - Ran a throttled GitHub code-search API pass over every solution file.
   - One normalized code snippet per file was queried with:
     - `language:Python`
     - `-repo:mik11231/python` (exclude this repository).
   - Stored machine-readable results in:
     - `.local_state/originality_github_scan.json`

2. **Manual triage of flagged files:**
   - Reviewed top-hit files with high `total_count`.
   - Pulled candidate files directly via GitHub API `repos/<owner>/<repo>/contents/<path>` (still no cloning).
   - Computed normalized similarity ratios against local files.

3. **Web-search sanity checks:**
   - Ran targeted web searches for distinctive code snippets from local solutions.
   - No direct third-party copy signals found in those checks.

### Coverage and results

- GitHub sweep outcomes:
  - `469` files: successful external search checks (`status=ok`)
  - `4` files: `no_snippet` (tiny/trivial Part 2 stubs):
    - `advent2015/Day25/day25_part2.py`
    - `advent2016/Day25/day25_part2.py`
    - `advent2018/Day10/day10_part2.py`
    - `advent2019/Day25/day25_part2.py`
- Flagged files with non-zero code-search hits were dominated by **generic Python idioms** (e.g. BFS neighbor loops, `map(int, line.split())`, common iteration patterns).
- Targeted content comparisons on the most suspicious-looking hits produced low similarity ratios (examples):
  - `advent2016/Day3/day3.py` vs `jtyr/advent-of-code-2016/03.py`: `0.053`
  - `advent2023/Day6/day6_part2.py` vs `DownDev/advent-of-code/2023/06-2.py`: `0.015`
  - `advent2019/Day7/day7.py` vs `EoinDavey/Competitive AdventOfCode2019/7.py`: `0.063`
  - `advent2015/Day5/day5.py` vs `JustinStitt/advent-of-code/2015/day-5/solve1.py`: `0.207` (small/problem-constrained code; still not near-copy).

### Additional internal consistency check

- Checked for exact duplicate normalized solution files inside this repo.
- Result: `0` duplicate-content clusters across all `473` solution files.

### Conclusion (2026-03-04)

- No evidence found of large-scale copying or near-identical pasted solutions from public repositories.
- Observed matches are consistent with common puzzle idioms and short, constrained algorithm patterns.

### Limitations

- Code search uses representative snippets, not formal AST-level plagiarism detection.
- Very short files can be hard to distinguish globally.
- Public web/code indexes are incomplete and continuously changing.
