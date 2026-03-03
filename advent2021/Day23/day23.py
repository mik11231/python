#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 23: Amphipod (Part 1)

Organise amphipods (A, B, C, D) into their correct side rooms with
minimum total energy.  Movement costs 1, 10, 100, or 1000 per step
depending on type.

Rules
-----
* The hallway has 11 spaces; amphipods may never stop on a room entrance
  (positions 2, 4, 6, 8).
* An amphipod in a room can move to any reachable hallway stop.
* An amphipod in the hallway can move into its destination room only when
  the room contains no amphipods of a different type.
* Once an amphipod stops in the hallway it will not move again until it
  can go directly into its room.

Algorithm
---------
Dijkstra on the full state space.  The state is (hallway, rooms) where
*hallway* is a length-11 tuple and each room is a tuple of characters
(top-to-bottom, i.e. closest to hallway first).
"""

import heapq
from pathlib import Path

ROOM_COLS = (2, 4, 6, 8)
HALL_STOPS = (0, 1, 3, 5, 7, 9, 10)
COSTS = {"A": 1, "B": 10, "C": 100, "D": 1000}
TARGET_ROOM = {"A": 0, "B": 1, "C": 2, "D": 3}
ROOM_TYPE = ("A", "B", "C", "D")


def parse_input(text: str) -> list[list[str]]:
    """Return four rooms, each a list of amphipods from top to bottom."""
    rooms: list[list[str]] = [[] for _ in range(4)]
    for line in text.strip().splitlines()[2:]:
        amps = [c for c in line if c in "ABCD"]
        if not amps:
            break
        for i, c in enumerate(amps):
            rooms[i].append(c)
    return rooms


def solve_amphipod(rooms: list[list[str]], room_size: int) -> int:
    """Return minimum energy to sort all amphipods into correct rooms.

    *rooms* is a list of four lists, each of length *room_size*, with
    amphipod characters ordered top-to-bottom.
    """
    hallway = tuple("." for _ in range(11))
    initial_rooms = tuple(tuple(r) for r in rooms)
    goal_rooms = tuple(tuple(ROOM_TYPE[i] for _ in range(room_size)) for i in range(4))

    start = (hallway, initial_rooms)
    goal_hall = hallway

    dist: dict[tuple, int] = {start: 0}
    pq: list[tuple[int, tuple]] = [(0, start)]

    while pq:
        cost, state = heapq.heappop(pq)
        if cost > dist.get(state, float("inf")):
            continue
        hall, rms = state
        if hall == goal_hall and rms == goal_rooms:
            return cost

        # --- moves: room -> hallway ---
        for ri in range(4):
            room = rms[ri]
            top_idx = None
            for j in range(room_size):
                if room[j] != ".":
                    top_idx = j
                    break
            if top_idx is None:
                continue

            amp = room[top_idx]
            if (
                TARGET_ROOM[amp] == ri
                and all(room[k] == ROOM_TYPE[ri] for k in range(top_idx, room_size))
            ):
                continue

            room_col = ROOM_COLS[ri]
            for h in HALL_STOPS:
                lo, hi = min(room_col, h), max(room_col, h)
                if any(hall[p] != "." for p in range(lo, hi + 1)):
                    continue

                steps = (top_idx + 1) + abs(room_col - h)
                new_cost = cost + steps * COSTS[amp]

                new_hall = list(hall)
                new_hall[h] = amp
                new_room = list(room)
                new_room[top_idx] = "."
                new_rms = list(rms)
                new_rms[ri] = tuple(new_room)
                new_state = (tuple(new_hall), tuple(new_rms))

                if new_cost < dist.get(new_state, float("inf")):
                    dist[new_state] = new_cost
                    heapq.heappush(pq, (new_cost, new_state))

        # --- moves: hallway -> room ---
        for h in HALL_STOPS:
            if hall[h] == ".":
                continue
            amp = hall[h]
            ri = TARGET_ROOM[amp]
            room = rms[ri]

            if any(
                room[k] != "." and room[k] != ROOM_TYPE[ri]
                for k in range(room_size)
            ):
                continue

            dest_idx = None
            for j in range(room_size - 1, -1, -1):
                if room[j] == ".":
                    dest_idx = j
                    break
            if dest_idx is None:
                continue

            room_col = ROOM_COLS[ri]
            lo, hi = min(h, room_col), max(h, room_col)
            if any(hall[p] != "." for p in range(lo, hi + 1) if p != h):
                continue

            steps = abs(h - room_col) + (dest_idx + 1)
            new_cost = cost + steps * COSTS[amp]

            new_hall = list(hall)
            new_hall[h] = "."
            new_room = list(room)
            new_room[dest_idx] = amp
            new_rms = list(rms)
            new_rms[ri] = tuple(new_room)
            new_state = (tuple(new_hall), tuple(new_rms))

            if new_cost < dist.get(new_state, float("inf")):
                dist[new_state] = new_cost
                heapq.heappush(pq, (new_cost, new_state))

    raise ValueError("No solution found")


def solve(input_path: str = "advent2021/Day23/d23_input.txt") -> int:
    """Return the minimum energy for the Part 1 (room-size 2) puzzle."""
    text = Path(input_path).read_text()
    rooms = parse_input(text)
    return solve_amphipod(rooms, room_size=2)


if __name__ == "__main__":
    print(f"Minimum energy (Part 1): {solve()}")
