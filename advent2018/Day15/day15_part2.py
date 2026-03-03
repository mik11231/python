from pathlib import Path
from day15 import load, run_combat


def solve(path: Path) -> int:
    """Find minimum elf attack power that yields no elf deaths."""
    atk = 4
    while True:
        grid, units = load(path, elf_attack=atk)
        rounds, hp_sum, elf_died = run_combat(grid, units, stop_on_elf_death=True)
        if not elf_died:
            return rounds * hp_sum
        atk += 1


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d15_input.txt')))
