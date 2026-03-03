from collections import deque
from dataclasses import dataclass
from pathlib import Path


ADJ = [(0, -1), (-1, 0), (1, 0), (0, 1)]  # reading-order adjacency


@dataclass
class Unit:
    """A combat unit (Elf or Goblin) with position, hp, and attack power."""

    kind: str
    x: int
    y: int
    attack: int = 3
    hp: int = 200
    alive: bool = True


def reading_key_pos(x: int, y: int) -> tuple[int, int]:
    return (y, x)


def load(path: Path, elf_attack: int = 3):
    """Parse map and units; replace unit chars in grid with floor '.'."""
    grid = [list(line.rstrip('\n')) for line in path.read_text().splitlines()]
    units = []
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch in 'EG':
                atk = elf_attack if ch == 'E' else 3
                units.append(Unit(ch, x, y, atk))
                grid[y][x] = '.'
    return grid, units


def occupied(units: list[Unit]) -> dict[tuple[int, int], Unit]:
    return {(u.x, u.y): u for u in units if u.alive}


def bfs_first_step(
    start: tuple[int, int],
    targets: set[tuple[int, int]],
    grid,
    blocked: set[tuple[int, int]],
):
    """Return first step from start toward nearest target with AoC tie-breaks.

    We BFS from start, expanding neighbors in reading order. For each reached cell,
    we carry the first step used to reach it. The first target discovered at minimum
    distance is selected in reading order automatically by BFS layering + neighbor order.
    """
    if not targets:
        return None

    q = deque()
    seen = {start}

    # Seed with one-step moves from start in reading order.
    sx, sy = start
    for dx, dy in ADJ:
        nx, ny = sx + dx, sy + dy
        np = (nx, ny)
        if np in blocked:
            continue
        if grid[ny][nx] != '.':
            continue
        seen.add(np)
        q.append((np, np, 1))  # (position, first_step, distance)

    best_dist = None
    candidates = []

    while q:
        pos, first_step, dist = q.popleft()

        if best_dist is not None and dist > best_dist:
            break

        if pos in targets:
            best_dist = dist
            candidates.append((pos, first_step))
            continue

        x, y = pos
        for dx, dy in ADJ:
            nx, ny = x + dx, y + dy
            np = (nx, ny)
            if np in seen or np in blocked or grid[ny][nx] != '.':
                continue
            seen.add(np)
            q.append((np, first_step, dist + 1))

    if not candidates:
        return None

    # Choose target in reading order, then first step in reading order.
    candidates.sort(key=lambda item: (item[0][1], item[0][0], item[1][1], item[1][0]))
    return candidates[0][1]


def run_combat(grid, units: list[Unit], stop_on_elf_death: bool = False):
    """Run combat and return (completed_rounds, hp_sum, elf_died_flag)."""
    rounds = 0

    while True:
        units.sort(key=lambda u: (u.y, u.x))

        for unit in units:
            if not unit.alive:
                continue

            enemies = [u for u in units if u.alive and u.kind != unit.kind]
            if not enemies:
                hp_sum = sum(u.hp for u in units if u.alive)
                return rounds, hp_sum, False

            occ = occupied(units)

            # If no adjacent enemy, try to move one step toward nearest reachable in-range square.
            adjacent_enemies = []
            for dx, dy in ADJ:
                p = (unit.x + dx, unit.y + dy)
                e = occ.get(p)
                if e and e.kind != unit.kind:
                    adjacent_enemies.append(e)

            if not adjacent_enemies:
                in_range = set()
                blocked = set(occ.keys()) - {(unit.x, unit.y)}
                for e in enemies:
                    for dx, dy in ADJ:
                        p = (e.x + dx, e.y + dy)
                        if p in blocked:
                            continue
                        if grid[p[1]][p[0]] == '.':
                            in_range.add(p)

                step = bfs_first_step((unit.x, unit.y), in_range, grid, blocked)
                if step is not None:
                    unit.x, unit.y = step

                occ = occupied(units)
                adjacent_enemies = []
                for dx, dy in ADJ:
                    p = (unit.x + dx, unit.y + dy)
                    e = occ.get(p)
                    if e and e.kind != unit.kind:
                        adjacent_enemies.append(e)

            if adjacent_enemies:
                # Attack enemy with lowest HP, tie by reading order.
                adjacent_enemies.sort(key=lambda e: (e.hp, e.y, e.x))
                target = adjacent_enemies[0]
                target.hp -= unit.attack
                if target.hp <= 0:
                    target.alive = False
                    if stop_on_elf_death and target.kind == 'E':
                        return rounds, 0, True

        rounds += 1


def solve(path: Path) -> int:
    grid, units = load(path, elf_attack=3)
    rounds, hp_sum, _ = run_combat(grid, units)
    return rounds * hp_sum


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d15_input.txt')))
