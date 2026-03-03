#!/usr/bin/env python3
"""Advent of Code 2022 Day 16 Part 2.

You and an elephant each have 26 minutes. Split valve-opening work between
two actors; for each partition of valves, take best human + best elephant
score and maximize their sum.
"""
from collections import deque
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
    """Solve Part 2: max combined pressure with two actors in 26 minutes each."""
    rates,g=parse(s)
    useful=[v for v,r in rates.items() if r>0]
    n=len(useful)
    idx={v:i for i,v in enumerate(useful)}
    all_d={v:dists(g,v) for v in g}

    best=[0]*(1<<n)

    def dfs(cur,time,mask,score):
        """Explore all valve orders; track best score per opened-valve mask."""
        if score>best[mask]: best[mask]=score
        for v in useful:
            bit=1<<idx[v]
            if mask&bit: continue
            t=time-all_d[cur][v]-1
            if t<=0: continue
            dfs(v,t,mask|bit,score+rates[v]*t)

    dfs('AA',26,0,0)

    # max_best[mask] = best score achievable using any subset of mask.
    max_best=best[:]
    for bit in range(n):
        for mask in range(1<<n):
            if mask&(1<<bit):
                alt=max_best[mask^(1<<bit)]
                if alt>max_best[mask]: max_best[mask]=alt

    full=(1<<n)-1
    ans=0
    for m in range(1<<n):
        ans=max(ans,best[m]+max_best[full^m])
    return ans


if __name__=='__main__':
    print(solve(Path(__file__).with_name('d16_input.txt').read_text()))
