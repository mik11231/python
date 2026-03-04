"""Allow running unified CLI as `python -m aoclib`."""

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
