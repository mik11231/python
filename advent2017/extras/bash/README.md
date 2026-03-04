# Bash X Solver

Native Bash per-day implementations focused on transparent control flow and measurable runtime behavior.

## Architecture

- One script per day in `days/dayN.sh`, each with a consistent CLI contract.
- Parsing and state transitions stay inside Bash (no language-wrapper delegation).
- Scripts report answer on stdout and runtime metrics on stderr for benchmark ingestion.

## Usage

```bash
bash solve.sh --day 22 --part 2 --input ../../Day22/d22_input.txt
bash solve.sh --all
```
