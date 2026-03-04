#!/usr/bin/env python3
"""Advent of Code 2017 Day 16 Part 2."""

from pathlib import Path


def dance(arr: list[str], ops: list[str]) -> list[str]:
    pos = {c: i for i, c in enumerate(arr)}
    for op in ops:
        t = op[0]
        if t == "s":
            x = int(op[1:])
            arr = arr[-x:] + arr[:-x]
            pos = {c: i for i, c in enumerate(arr)}
        elif t == "x":
            a, b = map(int, op[1:].split("/"))
            arr[a], arr[b] = arr[b], arr[a]
            pos[arr[a]] = a
            pos[arr[b]] = b
        else:
            a, b = op[1:].split("/")
            ia, ib = pos[a], pos[b]
            arr[ia], arr[ib] = arr[ib], arr[ia]
            pos[a], pos[b] = ib, ia
    return arr


def solve(s: str) -> str:
    ops = s.strip().split(",")
    arr = list("abcdefghijklmnop")
    seen = {}
    i = 0
    target = 1_000_000_000
    while i < target:
        k = "".join(arr)
        if k in seen:
            cyc = i - seen[k]
            rem = (target - i) % cyc
            for _ in range(rem):
                arr = dance(arr, ops)
            return "".join(arr)
        seen[k] = i
        arr = dance(arr, ops)
        i += 1
    return "".join(arr)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d16_input.txt").read_text(encoding="utf-8")))
