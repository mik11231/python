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
        """
        Run `__init__` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: self, x, y, d.
        - Produces side effects required by the caller (output/mutation/control flow).
        """
        self.x = x
        self.y = y
        self.d = d
        self.turn_state = 0  # 0=left, 1=straight, 2=right
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
    """Move one cart one cell and apply track-dependent direction changes."""
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


def first_crash(grid, carts) -> tuple[int, int]:
    """Run simulation until first collision and return its x,y coordinate."""
    while True:
        carts.sort(key=lambda c: (c.y, c.x))
        occupied = {(c.x, c.y): c for c in carts if c.alive}

        for cart in carts:
            if not cart.alive:
                continue
            occupied.pop((cart.x, cart.y), None)
            step_cart(cart, grid)
            pos = (cart.x, cart.y)
            if pos in occupied and occupied[pos].alive:
                return pos
            occupied[pos] = cart


def solve(grid, carts) -> str:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: grid, carts.
    - Returns the computed result for this stage of the pipeline.
    """
    x, y = first_crash(grid, carts)
    return f"{x},{y}"


if __name__ == '__main__':
    g, c = load(Path(__file__).with_name('d13_input.txt'))
    print(solve(g, c))
