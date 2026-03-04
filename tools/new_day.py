#!/usr/bin/env python3
"""Scaffold day files for an existing advent year folder."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def solve_template(year: int, day: int, part2: bool = False) -> str:
    suffix = " Part 2" if part2 else ""
    filename = f"d{day}_input.txt"
    return f'''#!/usr/bin/env python3
"""Advent of Code {year} Day {day}{suffix}."""

from pathlib import Path


def solve(s: str):
    """Implement solution and return final answer."""
    raise NotImplementedError("Implement day {day}{' part 2' if part2 else ''}")


if __name__ == "__main__":
    text = Path(__file__).with_name("{filename}").read_text(encoding="utf-8")
    print(solve(text))
'''


def test_template(day: int) -> str:
    return f'''#!/usr/bin/env python3
"""Example smoke tests for Day {day}."""

from pathlib import Path


def main() -> None:
    print("Add example assertions for Day {day}.")


if __name__ == "__main__":
    main()
'''


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create day scaffold files for adventYYYY/DayN")
    parser.add_argument("year", type=int)
    parser.add_argument("day", type=int)
    args = parser.parse_args(argv)

    if not (1 <= args.day <= 25):
        raise SystemExit("day must be between 1 and 25")

    day_dir = ROOT / f"advent{args.year}" / f"Day{args.day}"
    day_dir.mkdir(parents=True, exist_ok=True)

    write_if_missing(day_dir / f"d{args.day}_input.txt", "")
    write_if_missing(day_dir / f"d{args.day}_instructions.html", "")
    write_if_missing(day_dir / f"day{args.day}.py", solve_template(args.year, args.day, part2=False))
    write_if_missing(day_dir / f"day{args.day}_part2.py", solve_template(args.year, args.day, part2=True))
    write_if_missing(day_dir / "test_example.py", test_template(args.day))

    print(f"Scaffolded {day_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
