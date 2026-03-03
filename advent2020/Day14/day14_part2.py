#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 14: Docking Data (Part 2)

The mask is now applied to the *memory address* instead of the value:

  0 — the corresponding address bit is unchanged.
  1 — the corresponding address bit is overwritten with 1.
  X — the corresponding address bit is "floating" and takes both 0 and 1.

Each write fans out to all 2^(number of Xs) possible addresses.
Return the sum of all values in memory after the program completes.

Algorithm
---------
For each write, apply the 1-bits as an OR-mask to the address, then
enumerate every combination of the floating bits by iterating through
all subsets of the X-positions.
"""

from pathlib import Path

from day14 import parse_program


def _floating_addresses(base_addr: int, mask_str: str) -> list[int]:
    """Generate all addresses produced by the floating-bit mask."""
    floating_positions: list[int] = []
    for i, ch in enumerate(mask_str):
        bit = 35 - i
        if ch == "1":
            base_addr |= (1 << bit)
        elif ch == "X":
            floating_positions.append(bit)

    # Enumerate all 2^n combinations of floating bits
    addresses: list[int] = []
    for combo in range(1 << len(floating_positions)):
        addr = base_addr
        for j, bit in enumerate(floating_positions):
            if combo & (1 << j):
                addr |= (1 << bit)    # set this floating bit to 1
            else:
                addr &= ~(1 << bit)   # set this floating bit to 0
        addresses.append(addr)

    return addresses


def run_v2(program: list[tuple[str, ...]]) -> dict[int, int]:
    """Execute the program with version-2 (address masking) semantics."""
    memory: dict[int, int] = {}
    mask_str = "0" * 36

    for instr in program:
        if instr[0] == "mask":
            mask_str = instr[1]
        else:
            base_addr = int(instr[1])
            val = int(instr[2])
            for addr in _floating_addresses(base_addr, mask_str):
                memory[addr] = val

    return memory


def solve(input_path: str = "advent2020/Day14/d14_input.txt") -> int:
    """Read the docking program and return the sum of all memory values
    using version-2 (floating address) semantics."""
    program = parse_program(Path(input_path).read_text())
    memory = run_v2(program)
    return sum(memory.values())


if __name__ == "__main__":
    result = solve()
    print(f"Sum of all values in memory (v2): {result}")
