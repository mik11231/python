"""Advent of Code 2019 Day 25 Part 1.

Automates the text-adventure by:
1. Exploring all rooms via DFS.
2. Picking up non-dangerous items.
3. Brute-forcing inventory subsets at the security checkpoint.
"""

import itertools
import re
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from advent2019.intcode import IntcodeComputer


REV = {'north': 'south', 'south': 'north', 'west': 'east', 'east': 'west'}
DANGEROUS = {
    'infinite loop',
    'giant electromagnet',
    'molten lava',
    'escape pod',
    'photons',
}


class Droid:
    def __init__(self, program):
        """
        Run `__init__` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: self, program.
        - Produces side effects required by the caller (output/mutation/control flow).
        """
        self.vm = IntcodeComputer(program)

    def send(self, cmd: str) -> str:
        """
        Run `send` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: self, cmd.
        - Returns the computed result for this stage of the pipeline.
        """
        inp = [ord(c) for c in cmd + '\n']
        out, _ = self.vm.run(inp)
        return ''.join(chr(c) for c in out)

    def boot(self) -> str:
        """
        Run `boot` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: self.
        - Returns the computed result for this stage of the pipeline.
        """
        out, _ = self.vm.run([])
        return ''.join(chr(c) for c in out)


def parse_screen(txt: str):
    """
    Run `parse_screen` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: txt.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    room = None
    doors = []
    items = []

    m = re.search(r'== (.+?) ==', txt)
    if m:
        room = m.group(1)

    lines = txt.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip() == 'Doors here lead:':
            i += 1
            while i < len(lines) and lines[i].startswith('- '):
                doors.append(lines[i][2:])
                i += 1
            continue
        if lines[i].strip() == 'Items here:':
            i += 1
            while i < len(lines) and lines[i].startswith('- '):
                items.append(lines[i][2:])
                i += 1
            continue
        i += 1
    return room, doors, items


def solve(program):
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: program.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    d = Droid(program)
    txt = d.boot()
    room, doors, items = parse_screen(txt)

    graph = {}
    visited = set()
    inventory = []
    checkpoint = None
    checkpoint_exit = None

    def dfs(prev_dir=None):
        """
        Run `dfs` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: prev_dir.
        - Produces side effects required by the caller (output/mutation/control flow).
        """
        nonlocal room, doors, items, txt, checkpoint, checkpoint_exit
        cur_room = room
        if cur_room in visited:
            return
        visited.add(cur_room)
        graph.setdefault(cur_room, {})

        # Collect safe items in current room.
        for it in items:
            if it not in DANGEROUS:
                take_out = d.send(f'take {it}')
                inventory.append(it)
                txt = take_out

        # Refresh parsed room state after any item pickup.
        room2, doors2, items2 = parse_screen(txt)
        if room2:
            cur_room = room2
            room, doors, items = room2, doors2, items2

        for mv in doors:
            # Avoid stepping onto pressure floor during exploration.
            if cur_room == 'Security Checkpoint':
                checkpoint = cur_room
                checkpoint_exit = mv
                continue

            out = d.send(mv)
            nroom, ndoors, nitems = parse_screen(out)
            if not nroom:
                continue

            graph[cur_room][mv] = nroom
            graph.setdefault(nroom, {})[REV[mv]] = cur_room

            old_state = (room, doors, items, txt)
            room, doors, items, txt = nroom, ndoors, nitems, out
            if nroom not in visited:
                dfs(mv)

            back = d.send(REV[mv])
            room, doors, items = parse_screen(back)
            txt = back

    dfs()

    # Navigate to checkpoint from current room using BFS on discovered graph.
    def path_between(src, dst):
        """
        Run `path_between` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: src, dst.
        - Produces side effects required by the caller (output/mutation/control flow).
        """
        from collections import deque

        q = deque([(src, [])])
        seen = {src}
        while q:
            u, p = q.popleft()
            if u == dst:
                return p
            for mv, v in graph.get(u, {}).items():
                if v not in seen:
                    seen.add(v)
                    q.append((v, p + [mv]))
        raise RuntimeError('no path')

    current_room = room
    to_cp = path_between(current_room, checkpoint)
    for mv in to_cp:
        txt = d.send(mv)
    room, doors, items = parse_screen(txt)

    # Drop everything first.
    for it in inventory:
        d.send(f'drop {it}')

    # Try every subset at checkpoint.
    for r in range(len(inventory) + 1):
        for comb in itertools.combinations(inventory, r):
            for it in comb:
                d.send(f'take {it}')

            out = d.send(checkpoint_exit)
            if 'you are ejected back to the checkpoint' not in out.lower():
                m = re.search(r'(\d+)', out)
                if m:
                    return int(m.group(1))
                # Sometimes the code appears in the final line without explicit phrasing.
                nums = re.findall(r'\d+', out)
                if nums:
                    return int(nums[-1])

            for it in comb:
                d.send(f'drop {it}')

    raise RuntimeError('code not found')


if __name__ == '__main__':
    p = [int(x) for x in Path(__file__).with_name('d25_input.txt').read_text().strip().split(',')]
    print(solve(p))
