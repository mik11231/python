"""Advent of Code 2018 solution module."""

from pathlib import Path


DIRS = {
    '^': (0, -1),
    'v': (0, 1),
    '<': (-1, 0),
    '>': (1, 0),
}
LEFT = {'^': '<', '<': 'v', 'v': '>', '>': '^'}
RIGHT = {'^': '>', '>': 'v', 'v': '<', '<': '^'}


class Cart:
    """Track cart position, heading, and next turn state at intersections."""

    def __init__(self, x: int, y: int, d: str):
        self.x = x
        self.y = y
        self.d = d
        self.turn_state = 0
        self.alive = True


def load(path: Path):
    """Parse grid and carts, replacing cart symbols with underlying track."""
    grid = [list(line.rstrip('\n')) for line in path.read_text().splitlines()]
    carts = []
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch in DIRS:
                carts.append(Cart(x, y, ch))
                grid[y][x] = '|' if ch in '^v' else '-'
    return grid, carts


def step_cart(cart: Cart, grid):
    dx, dy = DIRS[cart.d]
    cart.x += dx
    cart.y += dy
    track = grid[cart.y][cart.x]

    if track == '/':
        cart.d = {'^': '>', 'v': '<', '<': 'v', '>': '^'}[cart.d]
    elif track == '\\':
        cart.d = {'^': '<', 'v': '>', '<': '^', '>': 'v'}[cart.d]
    elif track == '+':
        if cart.turn_state == 0:
            cart.d = LEFT[cart.d]
        elif cart.turn_state == 2:
            cart.d = RIGHT[cart.d]
        cart.turn_state = (cart.turn_state + 1) % 3


def last_cart(grid, carts) -> tuple[int, int]:
    """Run simulation removing colliding carts until only one remains."""
    while True:
        carts.sort(key=lambda c: (c.y, c.x))
        occupied = {(c.x, c.y): c for c in carts if c.alive}

        for cart in carts:
            if not cart.alive:
                continue
            occupied.pop((cart.x, cart.y), None)
            step_cart(cart, grid)
            pos = (cart.x, cart.y)
            other = occupied.get(pos)
            if other is not None and other.alive:
                cart.alive = False
                other.alive = False
                occupied.pop(pos, None)
            else:
                occupied[pos] = cart

        alive = [c for c in carts if c.alive]
        if len(alive) == 1:
            return alive[0].x, alive[0].y
        carts = alive


def solve(grid, carts) -> str:
    x, y = last_cart(grid, carts)
    return f"{x},{y}"


if __name__ == '__main__':
    g, c = load(Path(__file__).with_name('d13_input.txt'))
    print(solve(g, c))
