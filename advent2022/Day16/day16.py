#!/usr/bin/env python3
"""Advent of Code 2022 Day 16 Part 1.

Proboscidea Volcanium: valves with flow rates connected by tunnels. Maximize
total pressure released in 30 minutes by opening valves. Uses DFS with
memoization over (current valve, time left, opened valves bitmask).
"""
from collections import deque
from functools import lru_cache
from pathlib import Path
import re

def parse(s):
    """Parse valve definitions into flow rates and adjacency graph."""
    rates={}; g={}
    for ln in s.splitlines():
        if not ln: continue
        a,b=ln.split(';')
        v=a.split()[1]
        r=int(re.search(r'\d+',a).group())
        tos=[x.strip() for x in b.split('valve')[-1].replace('s ','').split(',')]
        rates[v]=r; g[v]=tos
    return rates,g

def dists(g,src):
    """BFS from src; return dict of valve -> shortest distance."""
    q=deque([(src,0)]); seen={src}; out={src:0}
    while q:
        u,d=q.popleft()
        for v in g[u]:
            if v not in seen:
                seen.add(v); out[v]=d+1; q.append((v,d+1))
    return out

def solve(s):
    """Solve Part 1: max pressure released in 30 minutes starting at AA."""
    rates,g=parse(s)
    useful=[v for v,r in rates.items() if r>0]
    idx={v:i for i,v in enumerate(useful)}
    all_d={v:dists(g,v) for v in g}

    @lru_cache(None)
    def dfs(cur,time,mask):
        """Recursive DFS: max pressure from cur with time and opened valves."""
        best=0
        for v in useful:
            bit=1<<idx[v]
            if mask&bit: continue
            t=time-all_d[cur][v]-1
            if t<=0: continue
            best=max(best, rates[v]*t + dfs(v,t,mask|bit))
        return best

    return dfs('AA',30,0)

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d16_input.txt').read_text()))
